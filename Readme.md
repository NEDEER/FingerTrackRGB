# Touchless LED Control with Hand Gestures! 🤚💡

![demo-gif](demo.gif)  
*Move index finger into box to toggle the LED!*

Control an LED connected to your Arduino without ever touching a button — simply move your hand in front of your webcam to turn the LED ON or OFF.

This project uses Python, OpenCV, and Arduino (via PyFirmata) to create a virtual button you "press" by pointing your finger in real space.  
Perfect for learning computer vision, automation, or adding some futuristic flair to your hardware!

---

## ✨ Features

- **Touchless** toggle for your LED using hand gesture detection
- **Virtual Button**: LED turns ON when you move your index finger into a box drawn on the video feed
- **Easy Hardware Integration**: Works with any Arduino board using PyFirmata
- **Customizable**: Tweak gestures or box to perform other tasks

---

## 🖥 Tech Stack / Requirements

- Python 3.7+
- [`opencv-python`](https://pypi.org/project/opencv-python/)
- [`cvzone`](https://pypi.org/project/cvzone/)
- [`pyfirmata`](https://pypi.org/project/pyfirmata/)

**Hardware:**
- Arduino board (Uno, Nano, Mega, etc.)
- LED, resistor, breadboard (Basic LED circuit)
- USB cable

---

## 🚀 Quick Start

### 1. Connect Your Arduino

- Plug in your Arduino to your computer via USB.
- Wire an LED + resistor to digital pin **8** (changeable in code).

### 2. Install Python Dependencies

```bash
pip install opencv-python cvzone pyfirmata
```

### 3. Find Your Arduino Port

- Windows: Check in Device Manager (e.g., `COM6`)
- macOS/Linux: Check `ls /dev/tty.*` (e.g., `/dev/ttyACM0`)
- Update the `port` variable in `main.py` as needed.

### 4. Run the Code

```bash
python main.py
```

---

## 🕹️ How To Use

1. A window pops up showing a colored box.
2. Move ONLY your index finger up (pointing gesture).
3. _Move your fingertip into the **box** drawn on screen._  
   - Inside the box: LED turns **ON** (box turns red)
   - Outside the box or finger down: LED turns **OFF** (box is green)
4. Press `q` to quit.

---

## 🛠️ Circuit Diagram

```
[Arduino Pin 8] ---[RESISTOR (~220Ω)]---[LED (+)]---[LED (-)]---[GND]
```

---

## 📝 File Descriptions

- `main.py` – Main touchless LED control script (hand tracking, virtual button, LED logic).
- `Readme.md` – You're reading it!

---

---

## 🤔 Troubleshooting

- **"Failed to grab frame from camera"**  
  Your webcam is unavailable or in use by another app.

- **"Could not find Arduino board"**  
  - Double-check the Arduino port in `main.py`
  - Close the Arduino IDE/Monitor before starting the script

- **LED Not Working?**
  - Check your wiring
  - Try toggling the pin output in a simple blink test

---

## 🙋‍♂️ Credits

- Hand tracking: [cvzone](https://github.com/cvzone/cvzone) ([HandTrackingModule](https://github.com/cvzone/cvzone/blob/master/cvzone/HandTrackingModule.py))
- Arduino communication: [pyfirmata](https://github.com/tino/pyFirmata)
- Concept & Code: [Your Name Here]

---

## 📄 License

MIT License

---

Enjoy your touchless hardware magic! 💡
If you build something cool, share it back!

