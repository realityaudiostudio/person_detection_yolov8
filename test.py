import cv2
import socket
import struct
import pickle
import numpy as np
from ultralytics import YOLO

# Load YOLO model
model = YOLO("best.pt")

# Set up socket
HOST = "0.0.0.0"  # Listen on all network interfaces
PORT = 5001
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Waiting for Raspberry Pi connection...")
conn, addr = server_socket.accept()
print("Connected by:", addr)

# Set up second socket for sending processed data
PI_HOST = addr[0]
PI_PORT = 5002
pi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pi_socket.connect((PI_HOST, PI_PORT))
print("Connected to Raspberry Pi for sending data.")

# Camera and object parameters
KNOWN_HEIGHT = 170  # Average human height in cm
FOCAL_LENGTH = 800  # Estimated focal length (adjust based on calibration)

try:
    while True:
        # Receive frame size
        data_size = struct.unpack(">L", conn.recv(4))[0]
        data = b""

        # Receive frame
        while len(data) < data_size:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet

        # Deserialize frame
        frame = pickle.loads(data)

        # Run YOLO detection
        results = model.predict(source=frame, show=False)

        person_found = False
        frame_width = frame.shape[1]

        for box in results[0].boxes:
            cls = int(box.cls[0])  # Class ID
            if cls == 0:  # 0 = Person class
                person_found = True
                x, y, w, h = box.xywh[0]  # Bounding box (x, y, width, height)
                cx = x + w / 2  # X-center of bounding box

                # Calculate deviation from center
                x_deviation = (cx - frame_width / 2) / (frame_width / 2)  # Normalized deviation (-1 to 1)
                
                # Estimate distance
                distance = (KNOWN_HEIGHT * FOCAL_LENGTH) / h

                # Prepare data to send
                data_to_send = f"{x_deviation:.2f},{distance:.2f}"
                pi_socket.sendall(data_to_send.encode())

        if not person_found:
            pi_socket.sendall(b"NO_PERSON")

except KeyboardInterrupt:
    print("❌ Stopped by user.")

finally:
    conn.close()
    pi_socket.close()
    server_socket.close()
    print("✅ Connection closed.")
