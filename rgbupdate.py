import cv2
import mediapipe as mp
import serial
import time

# ===================== USER SETTINGS =====================
SERIAL_PORT = "COM6"  # Change to your Arduino Nano COM port
BAUD_RATE = 9600
CAM_WIDTH = 640
CAM_HEIGHT = 480
# =========================================================

# Connect to Arduino
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # wait for Arduino reset

# Mediapipe Hands init
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

# RGB values
RGB_Values = [0, 0, 0]

# Box positions
BOX_WIDTH = 100
BOX_HEIGHT = 200
RED_BOX = (50, 150)   
GREEN_BOX = (200, 150)
BLUE_BOX = (350, 150)
RESET_BOX = (500, 150, 100, 60)  # x, y, w, h

# FPS calculation
prev_time = time.time()
fps = 0

# Map Y position inside a box to value 0-255
def y_to_value(y, box_y):
    val = int(((y - box_y) / BOX_HEIGHT) * 255)
    return max(0, min(255, val))

# Send values to Arduino
def send_rgb(r, g, b):
    rgb_string = f"{r},{g},{b}\n"
    arduino.write(rgb_string.encode())

with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                x = int(hand_landmarks.landmark[8].x * img.shape[1])  # index finger tip
                y = int(hand_landmarks.landmark[8].y * img.shape[0])

                # RED box
                if RED_BOX[0] < x < RED_BOX[0] + BOX_WIDTH and RED_BOX[1] < y < RED_BOX[1] + BOX_HEIGHT:
                    RGB_Values[0] = y_to_value(y, RED_BOX[1])
                # GREEN box
                elif GREEN_BOX[0] < x < GREEN_BOX[0] + BOX_WIDTH and GREEN_BOX[1] < y < GREEN_BOX[1] + BOX_HEIGHT:
                    RGB_Values[1] = y_to_value(y, GREEN_BOX[1])
                # BLUE box
                elif BLUE_BOX[0] < x < BLUE_BOX[0] + BOX_WIDTH and BLUE_BOX[1] < y < BLUE_BOX[1] + BOX_HEIGHT:
                    RGB_Values[2] = y_to_value(y, BLUE_BOX[1])
                # RESET button
                elif RESET_BOX[0] < x < RESET_BOX[0] + RESET_BOX[2] and RESET_BOX[1] < y < RESET_BOX[1] + RESET_BOX[3]:
                    RGB_Values = [0, 0, 0]

                send_rgb(*RGB_Values)

        # Draw RGB sliders
        cv2.rectangle(img, RED_BOX, (RED_BOX[0] + BOX_WIDTH, RED_BOX[1] + BOX_HEIGHT), (0, 0, 255), 2)
        cv2.rectangle(img, GREEN_BOX, (GREEN_BOX[0] + BOX_WIDTH, GREEN_BOX[1] + BOX_HEIGHT), (0, 255, 0), 2)
        cv2.rectangle(img, BLUE_BOX, (BLUE_BOX[0] + BOX_WIDTH, BLUE_BOX[1] + BOX_HEIGHT), (255, 0, 0), 2)

        # Fill sliders based on value
        cv2.rectangle(img, (RED_BOX[0], RED_BOX[1]),
                      (RED_BOX[0] + BOX_WIDTH, RED_BOX[1] + int((RGB_Values[0] / 255) * BOX_HEIGHT)), (0, 0, 255), -1)
        cv2.rectangle(img, (GREEN_BOX[0], GREEN_BOX[1]),
                      (GREEN_BOX[0] + BOX_WIDTH, GREEN_BOX[1] + int((RGB_Values[1] / 255) * BOX_HEIGHT)), (0, 255, 0), -1)
        cv2.rectangle(img, (BLUE_BOX[0], BLUE_BOX[1]),
                      (BLUE_BOX[0] + BOX_WIDTH, BLUE_BOX[1] + int((RGB_Values[2] / 255) * BOX_HEIGHT)), (255, 0, 0), -1)

        # Text values for each color
        cv2.putText(img, f"R: {RGB_Values[0]}", (RED_BOX[0], RED_BOX[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(img, f"G: {RGB_Values[1]}", (GREEN_BOX[0], GREEN_BOX[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(img, f"B: {RGB_Values[2]}", (BLUE_BOX[0], BLUE_BOX[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # Reset button
        cv2.rectangle(img, (RESET_BOX[0], RESET_BOX[1]),
                      (RESET_BOX[0] + RESET_BOX[2], RESET_BOX[1] + RESET_BOX[3]), (0, 255, 255), 2)
        cv2.putText(img, "Reset", (RESET_BOX[0] + 10, RESET_BOX[1] + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # Live mixed color preview
        preview_color = (RGB_Values[2], RGB_Values[1], RGB_Values[0])  # BGR for OpenCV
        cv2.putText(img, "Color:", (260, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        cv2.rectangle(img, (330, 5), (430, 45), preview_color, -1)

        # FPS calculation
        curr_time = time.time()
        fps = int(1 / (curr_time - prev_time))
        prev_time = curr_time
        cv2.putText(img, f"FPS: {fps}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.imshow("FingerTrackRGB - Arduino Nano", img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
arduino.close()
cv2.destroyAllWindows()
