import socket
import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Left motors (2 pins: forward and backward)
LEFT_FORWARD = 20
LEFT_BACKWARD = 21
# Right motors (2 pins: forward and backward)
RIGHT_FORWARD = 16
RIGHT_BACKWARD = 12

# Setup PWM for all pins
PWM_FREQ = 100

# Left motor PWM
GPIO.setup(LEFT_FORWARD, GPIO.OUT)
GPIO.setup(LEFT_BACKWARD, GPIO.OUT)
left_forward_pwm = GPIO.PWM(LEFT_FORWARD, PWM_FREQ)
left_backward_pwm = GPIO.PWM(LEFT_BACKWARD, PWM_FREQ)
left_forward_pwm.start(0)
left_backward_pwm.start(0)

# Right motor PWM
GPIO.setup(RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(RIGHT_BACKWARD, GPIO.OUT)
right_forward_pwm = GPIO.PWM(RIGHT_FORWARD, PWM_FREQ)
right_backward_pwm = GPIO.PWM(RIGHT_BACKWARD, PWM_FREQ)
right_forward_pwm.start(0)
right_backward_pwm.start(0)

# Motor control functions
def set_motor(pwm_forward, pwm_backward, speed):
    if speed > 0:
        pwm_forward.ChangeDutyCycle(min(speed, 100))
        pwm_backward.ChangeDutyCycle(0)
    elif speed < 0:
        pwm_forward.ChangeDutyCycle(0)
        pwm_backward.ChangeDutyCycle(min(abs(speed), 100))
    else:
        pwm_forward.ChangeDutyCycle(0)
        pwm_backward.ChangeDutyCycle(0)

def forward():
    set_motor(left_forward_pwm, left_backward_pwm, 70)
    set_motor(right_forward_pwm, right_backward_pwm, 70)

def backward():
    set_motor(left_forward_pwm, left_backward_pwm, -70)
    set_motor(right_forward_pwm, right_backward_pwm, -70)

def left():
    set_motor(left_forward_pwm, left_backward_pwm, -50)
    set_motor(right_forward_pwm, right_backward_pwm, 50)

def right():
    set_motor(left_forward_pwm, left_backward_pwm, 50)
    set_motor(right_forward_pwm, right_backward_pwm, -50)

def stop():
    set_motor(left_forward_pwm, left_backward_pwm, 0)
    set_motor(right_forward_pwm, right_backward_pwm, 0)

# Socket server setup
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on {HOST}:{PORT}")

try:
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected by {addr}")
        
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                    
                if data == 'w':
                    forward()
                    print("Moving Forward")
                elif data == 's':
                    backward()
                    print("Moving Backward")
                elif data == 'a':
                    left()
                    print("Turning Left")
                elif data == 'd':
                    right()
                    print("Turning Right")
                elif data == 'q':
                    stop()
                    print("Stopped")
                    
            except Exception as e:
                print(f"Error: {e}")
                break
                
        client_socket.close()
        stop()

except KeyboardInterrupt:
    print("Shutting down...")
finally:
    stop()
    left_forward_pwm.stop()
    left_backward_pwm.stop()
    right_forward_pwm.stop()
    right_backward_pwm.stop()
    GPIO.cleanup()
    server_socket.close()