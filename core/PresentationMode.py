import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui
import mouse 

##########################
wCam, hCam = 640, 480 
frameR = 100 # Frame Reduction
smoothening = 9
#########################
prev_scroll = 0
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0


# Try camera index 1 (common if you have multiple cameras); fall back to 0 if unavailable
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    cap.release()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Unable to open camera (tried index 1 and 0). Check camera connection or change the index.")

cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
double_click_done = False 
prev_x = 0
slide_change_time = 0
cooldown = 1.0
# print(wScr, hScr)
prev_motion_x = None
motion_time = 0
motion_cooldown = 2# seconds
motion_threshold = 80

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    # guard: if read failed or returned an empty frame, try to reinitialize camera and continue
    if not success or img is None or (hasattr(img, 'size') and img.size == 0):
        print("Warning: empty frame captured. Reinitializing camera and retrying...")
        try:
            cap.release()
        except Exception:
            pass
        # try to reopen default camera index 0
        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)
        time.sleep(0.2)
        continue

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # 2. Get the tip of the index and middle fingers
    

   
    
    # 3. Check which fingers are up
    fingers = detector.fingersUp()
    # print(fingers)
    
   
    
        

# -----------------------------
    if fingers == [0, 1, 1, 0, 0]:
        pyautogui.press('right')
        time.sleep(1.5)
        cv2.putText(img, "→ Next Slide", (200, 100),
            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
               

            # ✌️ Two fingers up → Previous Slide
    elif fingers == [0, 1, 0, 0, 0]:
        pyautogui.press('left')
        time.sleep(1.5)
        cv2.putText(img, "← Previous Slide", (150, 100),
            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    (255, 0, 0), 3)
    # 12. Display
    # only show valid images
    if img is not None and (not hasattr(img, 'size') or img.size > 0):
        cv2.imshow("Image", img)
    # allow exit with Esc
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()            