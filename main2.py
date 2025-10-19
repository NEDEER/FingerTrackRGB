import cv2
from cvzone.HandTrackingModule import HandDetector
import pyfirmata
import time

# --- Arduino Setup ---
port = 'COM6'  # Change to your Arduino port
board = pyfirmata.Arduino(port)
led_pin = board.get_pin('d:8:o')  # Digital pin 8 for relay/LED

# --- Hand Detector Setup ---
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

led_state = False
last_toggle_time = 0
cooldown = 1  # seconds between toggles

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)  # With draw=True by default

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)  # List of 5 ints (1=open, 0=closed)

        # Example Gesture: All fingers up => Toggle LED
        if fingers == [0, 1, 0, 0, 0]:  # Only index finger up
            current_time = time.time()
            if current_time - last_toggle_time > cooldown:
                led_state = not led_state
                led_pin.write(1 if led_state else 0)
                last_toggle_time = current_time

        # Display LED state
        color = (0, 255, 0) if not led_state else (0, 0, 255)
        label = "LED 1"
        cv2.putText(img, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.rectangle(img, (30, 20), (150, 60), color, -1)
        cv2.putText(img, label, (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Touchless LED Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
