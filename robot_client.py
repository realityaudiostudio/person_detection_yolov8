import socket
import keyboard
import time

# Replace with your Raspberry Pi's IP address
PI_IP = '192.168.1.xxx'  # Change this to your Pi's IP
PORT = 5000

def connect_to_robot():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((PI_IP, PORT))
    return client_socket

def main():
    print("Connecting to robot...")
    try:
        sock = connect_to_robot()
        print("Connected! Use WASD to control (Q to stop, Ctrl+C to exit)")
        
        while True:
            if keyboard.is_pressed('w'):
                sock.send('w'.encode())
                time.sleep(0.1)
            elif keyboard.is_pressed('s'):
                sock.send('s'.encode())
                time.sleep(0.1)
            elif keyboard.is_pressed('a'):
                sock.send('a'.encode())
                time.sleep(0.1)
            elif keyboard.is_pressed('d'):
                sock.send('d'.encode())
                time.sleep(0.1)
            elif keyboard.is_pressed('q'):
                sock.send('q'.encode())
                time.sleep(0.1)
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.send('q'.encode())  # Stop the robot
        sock.close()
        print("Disconnected")

if __name__ == "__main__":
    main()