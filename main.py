import cv2
import mediapipe as mp
import urllib.request
import os
import time
import numpy as np
import pyautogui
import math

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

SCREEN_W, SCREEN_H = pyautogui.size()
FRAME_MARGIN = 100
SMOOTHING = 5

prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0

left_clicked = False
right_clicked = False
is_dragging = False

model_path = 'hand_landmarker.task'
if not os.path.exists(model_path):
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    urllib.request.urlretrieve(url, model_path)

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)

HAND_CONNECTIONS = [
    (0,1), (1,2), (2,3), (3,4),
    (0,5), (5,6), (6,7), (7,8),
    (5,9), (9,10), (10,11), (11,12),
    (9,13), (13,14), (14,15), (15,16),
    (13,17), (0,17), (17,18), (18,19), (19,20)
]

cap = cv2.VideoCapture(0)

with HandLandmarker.create_from_options(options) as landmarker:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        gesture_text = "NEUTRAL"
        
        cv2.rectangle(
            frame, 
            (FRAME_MARGIN, FRAME_MARGIN), 
            (w - FRAME_MARGIN, h - FRAME_MARGIN), 
            (0, 255, 255), 
            2
        )
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp_ms = int(time.time() * 1000)
        result = landmarker.detect_for_video(mp_image, timestamp_ms)
        
        if result.hand_landmarks:
            for hand in result.hand_landmarks:
                for connection in HAND_CONNECTIONS:
                    p1 = hand[connection[0]]
                    p2 = hand[connection[1]]
                    x1, y1 = int(p1.x * w), int(p1.y * h)
                    x2, y2 = int(p2.x * w), int(p2.y * h)
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                thumb_tip = hand[4]
                index_tip = hand[8]
                index_pip = hand[6]
                middle_tip = hand[12]
                middle_pip = hand[10]
                ring_tip = hand[16]
                pinky_tip = hand[20]
                
                ix, iy = int(index_tip.x * w), int(index_tip.y * h)
                tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)
                mx, my = int(middle_tip.x * w), int(middle_tip.y * h)

                index_up = index_tip.y < index_pip.y
                middle_up = middle_tip.y < middle_pip.y
                ring_up = ring_tip.y < hand[14].y
                pinky_up = pinky_tip.y < hand[18].y

                left_click_dist = math.hypot(tx - ix, ty - iy)
                two_finger_dist = math.hypot(mx - ix, my - iy)

                if index_up and middle_up and not ring_up and not pinky_up and two_finger_dist >= 40:
                    gesture_text = "SCROLLING"
                    cv2.circle(frame, (ix, iy), 10, (255, 255, 0), cv2.FILLED)
                    cv2.circle(frame, (mx, my), 10, (255, 255, 0), cv2.FILLED)
                    
                    if iy < h // 2 - 30:
                        pyautogui.scroll(40)
                    elif iy > h // 2 + 30:
                        pyautogui.scroll(-40)

                elif index_up and middle_up and two_finger_dist < 35:
                    gesture_text = "RIGHT CLICK"
                    cv2.circle(frame, (mx, my), 12, (255, 0, 0), cv2.FILLED)
                    if not right_clicked:
                        pyautogui.rightClick()
                        right_clicked = True
                else:
                    right_clicked = False

                if index_up and not middle_up:
                    screen_target_x = np.interp(ix, (FRAME_MARGIN, w - FRAME_MARGIN), (0, SCREEN_W))
                    screen_target_y = np.interp(iy, (FRAME_MARGIN, h - FRAME_MARGIN), (0, SCREEN_H))

                    curr_x = prev_x + (screen_target_x - prev_x) / SMOOTHING
                    curr_y = prev_y + (screen_target_y - prev_y) / SMOOTHING
                    pyautogui.moveTo(curr_x, curr_y)
                    prev_x, prev_y = curr_x, curr_y

                    if left_click_dist < 30:
                        gesture_text = "DRAG / CLICK"
                        cv2.circle(frame, (ix, iy), 12, (0, 255, 0), cv2.FILLED)
                        if not is_dragging:
                            pyautogui.mouseDown()
                            is_dragging = True
                    else:
                        if is_dragging:
                            pyautogui.mouseUp()
                            is_dragging = False
                        cv2.circle(frame, (ix, iy), 10, (255, 0, 255), cv2.FILLED)

        cv2.rectangle(frame, (10, 10), (360, 60), (0, 0, 0), -1)
        cv2.putText(frame, f"Gesture: {gesture_text}", (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Virtual Mouse - Tracking", frame)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            if is_dragging:
                pyautogui.mouseUp()
            break

cap.release()
cv2.destroyAllWindows()