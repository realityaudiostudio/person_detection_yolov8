import cv2
import socket
import struct
import pickle

# Set up the camera
cap = cv2.VideoCapture(0)  # Use the Raspberry Pi camera

# Set up socket
HOST = "192.168.33.30"  # Change to your laptop's IP address
PORT = 5001  # Port to send video to laptop
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected to Laptop.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Serialize frame
        data = pickle.dumps(frame)
        size = struct.pack(">L", len(data))

        # Send frame size, then frame
        client_socket.sendall(size + data)

except KeyboardInterrupt:
    print("❌ Stopped by user.")
except Exception as e:
    print(f"Error: {e}")

finally:
    cap.release()
    client_socket.close()
    print("✅ Camera stream stopped.")