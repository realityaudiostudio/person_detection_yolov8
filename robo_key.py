import curses
from gpiozero import OutputDevice, PWMOutputDevice
import time

# Define motor control pins
IN3 = OutputDevice(12)  # GPIO 12 (Pin 32)
IN4 = OutputDevice(16)  # GPIO 16 (Pin 36)
IN1 = OutputDevice(20)
IN2 = OutputDevice(21)
ENB = PWMOutputDevice(18)
ENB2 = PWMOutputDevice(13)  # GPIO 18 (Pin 12)
#second motor sessions
IN1_2 = OutputDevice(6)
IN2_2 = OutputDevice(5)
IN3_2 = OutputDevice(22)
IN4_2 = OutputDevice(27)
ENA_2 = PWMOutputDevice(23)
ENB_2 = PWMOutputDevice(24)

# Initial speed
speed = 1.0
ENB.value = speed
ENB2.value = speed
ENA_2.value = speed
ENB_2.value = speed

def move_forward():
    print("Moving Forward")
    IN3.on()
    IN4.off()
    IN1.off()
    IN2.on()
    IN1_2.on()
    IN2_2.off()
    IN3_2.off()
    IN4_2.on()

def move_backward():
    print("Moving Backward")
    IN3.off()
    IN4.on()
    IN1.on()
    IN2.off()
    IN1_2.off()
    IN2_2.on()
    IN3_2.on()
    IN4_2.off()

def rotate_left():
    print("Rotating Left")
    # Left wheels move backward, right wheels move forward
    IN3.off()  # Left motor backward
    IN4.on()
    IN1.on()
    IN2.off()

    IN1_2.on()  # Right motor forward
    IN2_2.off()
    IN3_2.off()
    IN4_2.on()

def rotate_right():
    print("Rotating Right")
    # Left wheels move forward, right wheels move backward
    IN3.on()  # Left motor forward
    IN4.off()
    IN1.off()
    IN2.on()

    IN1_2.off()  # Right motor backward
    IN2_2.on()
    IN3_2.on()
    IN4_2.off()

def stop_motor():
    print("Stopping Motor")
    IN3.off()
    IN4.off()
    IN1.off()
    IN2.off()
    IN1_2.off()
    IN2_2.off()
    IN3_2.off()
    IN4_2.off()

def increase_speed():
    global speed
    if speed < 1.0:
        speed += 0.1
        ENB.value = speed
        ENB2.value = speed
        ENA_2.value = speed
        ENB_2.value = speed
        print(f"Speed increased: {speed:.1f}")

def decrease_speed():
    global speed
    if speed > 0.1:
        speed -= 0.1
        ENB.value = speed
        ENB2.value = speed
        ENA_2.value = speed
        ENB_2.value = speed
        print(f"Speed decreased: {speed:.1f}")

def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)  # Non-blocking input
    stdscr.addstr(0, 0, "Use 'W' to move forward, 'S' to move backward, 'Q' to stop.")
    stdscr.addstr(1, 0, "Use '+' to increase speed, '-' to decrease speed. Press 'X' to exit.")

    while True:
        key = stdscr.getch()

        if key == ord('w'):
            move_forward()
        elif key == ord('s'):
            move_backward()
        elif key == ord('a'):
            rotate_left()
        elif key == ord('d'):
            rotate_right()
        elif key == ord('q'):
            stop_motor()
        elif key == ord('+'):
            increase_speed()
        elif key == ord('-'):
            decrease_speed()
        elif key == ord('x'):
            stop_motor()
            break  # Exit loop

        time.sleep(0.1)  # Reduce CPU usage

# Run the curses UI
curses.wrapper(main)

