from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO("best.pt")  # Ensure best.pt is in the same directory

# Access device camera (0 = default webcam)
cap = cv2.VideoCapture(0)

# Set camera resolution (optional)
cap.set(3, 1080)  # Width
cap.set(4, 720)  # Height

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # If no frame is captured, exit

        # Run YOLO detection on the frame
        results = model.predict(source=frame, show=False)

        num_persons = 0
        frame_width = frame.shape[1]

        # Process detections
        for box in results[0].boxes:
            cls = int(box.cls[0])  # Class ID
            if cls == 0:  # 0 = Person class
                num_persons += 1
                x, y, w, h = box.xywh[0]  # Bounding box (x, y, width, height)
                cx = x + w / 2  # X-center of bounding box

                # Determine position
                if cx < frame_width / 3:
                    position = "Left"
                elif cx > 2 * frame_width / 3:
                    position = "Right"
                else:
                    position = "Center"

                # Draw bounding box
                x1, y1, x2, y2 = box.xyxy[0]  # Convert to (x1, y1, x2, y2) format
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, position, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Add person count
        cv2.putText(frame, f"Persons: {num_persons}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Show frame
        cv2.imshow("Live Person Detection", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("❌ Stopped by user.")

# Release resources
cap.release()
cv2.destroyAllWindows()
print("✅ Camera stream stopped.")
