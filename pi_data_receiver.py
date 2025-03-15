import socket

# Set up socket
HOST = "0.0.0.0"  # Listen on all network interfaces
PORT = 5002
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Waiting for data from Laptop...")

conn, addr = server_socket.accept()
print("Connected to:", addr)

try:
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        if data == "NO_PERSON":
            print("No person detected.")
        else:
            x_deviation, distance = map(float, data.split(","))
            print(f"x_deviation: {x_deviation:.2f}, Distance: {distance:.2f} cm")

except KeyboardInterrupt:
    print("❌ Stopped by user.")

finally:
    conn.close()
    server_socket.close()
    print("✅ Connection closed.")
# This script runs on the Raspberry Pi and receives data from the Laptop.
# It listens for incoming connections on port 5002 and prints the received data.