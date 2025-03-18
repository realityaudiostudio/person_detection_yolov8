import socket

# Set up socket to receive data from Laptop
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5002  # Matches PI_PORT in laptop script
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
except Exception as e:
    print(f"Error: {e}")

finally:
    conn.close()
    server_socket.close()
    print("✅ Connection closed.")