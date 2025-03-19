import cv2
import socket
import struct
import pickle
import numpy as np
import time
from ultralytics import YOLO

# Load YOLO model
model = YOLO("best.pt")

# Set up socket to receive video from Raspberry Pi
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5001  # Matches sender port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Waiting for Raspberry Pi connection...")
conn, addr = server_socket.accept()
print("Connected by:", addr)

# Set up socket to send results back to Raspberry Pi
PI_HOST = addr[0]  # Raspberry Pi's IP
PI_PORT = 5002  # Matches receiver port
pi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pi_socket.connect((PI_HOST, PI_PORT))
print("Connected to Raspberry Pi for sending data.")

# Camera and object parameters
KNOWN_HEIGHT = 170  # Average human height in cm
FOCAL_LENGTH = 800  # Adjust based on calibration

# Processing control parameters
frame_count = 0
process_every_n_frames = 2  # Process every N frames
last_result = None  # Store last detection result

try:
    while True:
        start_time = time.time()
        
        # Receive frame size
        data_size_bytes = conn.recv(4)
        if not data_size_bytes:
            print("No data received, connection may be closed")
            break
            
        data_size = struct.unpack(">L", data_size_bytes)[0]
        data = b""
        
        # Receive frame with timeout
        bytes_remaining = data_size
        while bytes_remaining > 0:
            chunk = conn.recv(min(bytes_remaining, 4096))
            if not chunk:
                raise Exception("Connection broken during frame receive")
            data += chunk
            bytes_remaining -= len(chunk)

        # Deserialize frame
        compressed_frame = pickle.loads(data)
        frame = cv2.imdecode(np.frombuffer(compressed_frame, dtype=np.uint8), cv2.IMREAD_COLOR)
        
        # Display the frame
        cv2.imshow("Raspberry Pi Camera Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Increment frame counter and process selectively
        frame_count += 1
        if frame_count % process_every_n_frames == 0:
            # Run YOLO detection
            results = model.predict(source=frame, show=False, conf=0.5)
            
            person_found = False
            frame_width = frame.shape[1]
            
            for box in results[0].boxes:
                cls = int(box.cls[0])  # Class ID
                if cls == 0:  # 0 = Person class
                    person_found = True
                    x, y, w, h = box.xywh[0]  # Bounding box (x, y, width, height)
                    cx = x  # X-center of bounding box
                    
                    # Calculate deviation from center
                    x_deviation = (cx - frame_width / 2) / (frame_width / 2)  # Normalized (-1 to 1)
                    
                    # Estimate distance
                    distance = (KNOWN_HEIGHT * FOCAL_LENGTH) / h
                    
                    # Prepare data to send
                    data_to_send = f"{x_deviation:.2f},{distance:.2f}"
                    pi_socket.sendall(data_to_send.encode())
                    last_result = data_to_send
                    break  # Process only the first person detected
            
            if not person_found:
                pi_socket.sendall(b"NO_PERSON")
                last_result = "NO_PERSON"
        
        # Optional: Add a small delay to control processing rate
        processing_time = time.time() - start_time
        if processing_time < 0.03:  # Aim for ~30fps max
            time.sleep(0.03 - processing_time)
        
        # Print FPS every 30 frames
        if frame_count % 30 == 0:
            fps = 1.0 / (time.time() - start_time)
            print(f"FPS: {fps:.2f}, Last result: {last_result}")

except KeyboardInterrupt:
    print("❌ Stopped by user.")
except Exception as e:
    print(f"Error: {e}")

finally:
    conn.close()
    pi_socket.close()
    server_socket.close()
    cv2.destroyAllWindows()
    print("✅ Connection closed.")