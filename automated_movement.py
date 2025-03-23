from ultralytics import YOLO
import cv2
from gpiozero import OutputDevice, PWMOutputDevice
import time
import threading

# Define motor control pins
IN3 = OutputDevice(12)  # Left motor
IN4 = OutputDevice(16)
IN1 = OutputDevice(20)
IN2 = OutputDevice(21)
ENB = PWMOutputDevice(18)
ENB2 = PWMOutputDevice(13)

IN1_2 = OutputDevice(6)  # Right motor
IN2_2 = OutputDevice(5)
IN3_2 = OutputDevice(22)
IN4_2 = OutputDevice(27)
ENA_2 = PWMOutputDevice(23)
ENB_2 = PWMOutputDevice(24)

# Initial speed
speed = 0.7
ENB.value = speed
ENB2.value = speed
ENA_2.value = speed
ENB_2.value = speed

# Load YOLO model
model = YOLO("best.pt")

# Camera parameters
cap = cv2.VideoCapture(0)
cap.set(3, 1080)  # Width
cap.set(4, 720)   # Height
KNOWN_HEIGHT = 170  # Average human height in cm
FOCAL_LENGTH = 800  # Estimated focal length
MIN_DISTANCE = 100  # Minimum distance in cm to maintain
MAX_DISTANCE = 200  # Maximum distance to start moving

# Global variables for robot control
current_position = "Center"
current_distance = 0
robot_running = True

def move_forward():
    IN3.on()
    IN4.off()
    IN1.off()
    IN2.on()
    IN1_2.on()
    IN2_2.off()
    IN3_2.off()
    IN4_2.on()

def move_backward():
    IN3.off()
    IN4.on()
    IN1.on()
    IN2.off()
    IN1_2.off()
    IN2_2.on()
    IN3_2.on()
    IN4_2.off()

def rotate_left():
    IN3.off()  # Left motor backward
    IN4.on()
    IN1.on()
    IN2.off()
    IN1_2.on()  # Right motor forward
    IN2_2.off()
    IN3_2.off()
    IN4_2.on()

def rotate_right():
    IN3.on()  # Left motor forward
    IN4.off()
    IN1.off()
    IN2.on()
    IN1_2.off()  # Right motor backward
    IN2_2.on()
    IN3_2.on()
    IN4_2.off()

def stop_motor():
    IN3.off()
    IN4.off()
    IN1.off()
    IN2.off()
    IN1_2.off()
    IN2_2.off()
    IN3_2.off()
    IN4_2.off()

def robot_control():
    global current_position, current_distance, robot_running
    
    while robot_running:
        if current_distance == 0:  # No person detected
            stop_motor()
        else:
            # Adjust based on position
            if current_position == "Left":
                rotate_left()
            elif current_position == "Right":
                rotate_right()
            else:  # Center
                # Adjust based on distance
                if current_distance < MIN_DISTANCE:
                    move_backward()
                elif current_distance > MAX_DISTANCE:
                    move_forward()
                else:
                    stop_motor()
        time.sleep(0.1)

def main():
    global current_position, current_distance, robot_running
    
    # Start robot control in a separate thread
    robot_thread = threading.Thread(target=robot_control)
    robot_thread.start()

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = model.predict(source=frame, show=False)
            num_persons = 0
            frame_width = frame.shape[1]

            # Reset distance if no person detected
            current_distance = 0

            # Process detections
            for box in results[0].boxes:
                if int(box.cls[0]) == 0:  # Person class
                    num_persons += 1
                    x, y, w, h = box.xywh[0]
                    cx = x + w / 2

                    # Calculate distance
                    distance = (KNOWN_HEIGHT * FOCAL_LENGTH) / h
                    current_distance = distance

                    # Determine position
                    if cx < frame_width / 3:
                        current_position = "Left"
                    elif cx > 2 * frame_width / 3:
                        current_position = "Right"
                    else:
                        current_position = "Center"

                    # Draw bounding box and text
                    x1, y1, x2, y2 = box.xyxy[0]
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    text = f"{current_position}, {distance:.1f} cm"
                    cv2.putText(frame, text, (int(x1), int(y1) - 10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    break  # Process only the first detected person

            # Display person count
            cv2.putText(frame, f"Persons: {num_persons}", (20, 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow("Person Following Robot", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("❌ Stopped by user.")
    
    # Cleanup
    robot_running = False
    robot_thread.join()
    stop_motor()
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Program stopped.")

if __name__ == "__main__":
    main()