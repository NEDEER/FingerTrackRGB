"""
Touchless LED Control with Hand Gestures! 🤚💡

Control an LED without pressing a single button — just by moving your hand in the air!
This project uses Python, OpenCV, and Arduino to create a virtual button that detects hand gestures to turn the LED on or off.

✨ Tech Stack:
🖥 Python + OpenCV for real-time hand tracking
🤖 Arduino (via PyFirmata) for LED control
⚡ Simple and fun gesture-based interaction

🔧 Key Features:
- Touchless LED control
- Real-time gesture detection
- Easy to customize for other devices
"""

import cv2
from cvzone.HandTrackingModule import HandDetector
import pyfirmata
import time

# --- Arduino Setup ---
port = 'COM6'  # Change to your Arduino port
board = pyfirmata.Arduino(port)
led_pin = board.get_pin('d:8:o')  # Digital pin 8 for LED

# --- Hand Detector Setup ---
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Define the virtual button area (x1, y1, x2, y2)
box_start = (20, 20)
box_end = (150, 70)

print("🤚💡 Touchless LED Control Started! Move your index finger into the box to turn the LED ON.")
print("Press 'q' to quit.")

while True:
    success, img = cap.read()
    if not success:
        print("Failed to grab frame from camera.")
        break

    hands, img = detector.findHands(img)  # Draw hand landmarks

    led_state = False  # Default: LED off

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)  # [Thumb, Index, Middle, Ring, Pinky]

        # Gesture: Only index finger up
        if fingers == [0, 1, 0, 0, 0]:
            # Get index finger tip position
            index_tip = hand['lmList'][8][:2]  # (x, y)
            x, y = int(index_tip[0]), int(index_tip[1])

            # Check if index finger is inside the virtual button box
            if box_start[0] <= x <= box_end[0] and box_start[1] <= y <= box_end[1]:
                led_state = True

    # Write LED state to Arduino
    led_pin.write(1 if led_state else 0)

    # Draw the virtual button and LED status
    color = (0, 0, 255) if led_state else (0, 255, 0)  # Red if ON, Green if OFF
    cv2.rectangle(img, box_start, box_end, color, -1)
    status_text = "ON" if led_state else "OFF"
    cv2.putText(img, f"LED: {status_text}", (box_start[0]+10, box_start[1]+40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display instructions on the frame
    cv2.putText(img, "Move index finger into box", (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 50, 255), 2)

    cv2.imshow("Touchless LED Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
