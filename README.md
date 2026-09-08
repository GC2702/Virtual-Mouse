# 👆 Gesture-Controlled Virtual Mouse

A touchless, AI-powered virtual mouse application that allows you to control your computer's cursor and perform mouse operations using hand gestures via your webcam. 

Built with Python, OpenCV, and Google's MediaPipe framework.

## ✨ Features & Gesture Controls

*   **Move Cursor:** Point with your **Index Finger** (👆) to move the mouse around the screen.
*   **Left Click:** Pinch your **Thumb and Index Finger** (🤏) together.
*   **Drag and Drop:** Hold the pinch (👌) and move your hand to drag, then release the pinch to drop.
*   **Right Click:** Bring your **Index and Middle Fingers** together (✌️ closed).
*   **Scroll Up/Down:** Hold your **Index and Middle Fingers** up and apart (✌️ open). Move your hand above the center of the screen to scroll up, and below the center to scroll down.
*   **Pause/Neutral:** Make a **Fist** (✊) to pause tracking and easily move your hand away.

## 🛠️ Tech Stack

*   **Python 3**
*   **OpenCV** (Camera and UI feedback)
*   **MediaPipe Tasks API** (Real-time hand landmark tracking)
*   **PyAutoGUI** (OS-level mouse control)
*   **NumPy** (Screen coordinate mapping)

## 🚀 How to Run

1. Clone this repository:
   ```bash
   git clone [https://github.com/GC2702/Virtual-Mouse.git](https://github.com/GC2702/Virtual-Mouse.git)
   cd Virtual-Mouse
Create a virtual environment and activate it:

Bash
python -m venv venv
venv\Scripts\activate

Install the dependencies:

Bash
pip install -r requirements.txt

Run the application:

Bash
python main.py
