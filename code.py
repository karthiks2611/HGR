import MySQLdb
import time
import cv2
import mediapipe as mp
import requests
import math



db = MySQLdb.connect(
    host="Your host here",
    user="Username here",
    passwd="password here",
    db="database here"
)

curr = db.cursor()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
prev_time = 0
# Connecting to mobile cam
mob_cam = 'http://XXX.XXX.XXX.XXX:4747/video'
lap_cam = 0

cap = cv2.VideoCapture(lap_cam)

# cap.set(3, 1920)
# cap.set(4, 1080)
rate = 5



def FPS():
    global prev_time
    current_time = time.time()
    fps = 1/(current_time - prev_time)
    prev_time = current_time
    return fps

def distance(x1, y1, x2, y2):
    return math.sqrt(abs((x1 - x2)*2 + (y1 - y2)*2))

X1 = 1
Y1 = 1

global prev_off_time
global prev_ch_time 
global prev_mute 

prev_off_time = 0
prev_ch_time  = 0
prev_mute = 0

with mp_hands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5, max_num_hands=1) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    # print(results.multi_hand_landmarks)
    # print(results.multi_handedness)

    #image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks == None:
      X1 = 1
      Y1 = 1
    

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        h, w, _ = image.shape

        current_time = time.time()

        for idx, classificaion in enumerate(results.multi_handedness):
            if classificaion.classification[0].label == "Left":            
                thtx = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*h)
                thty = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*w)

                itx = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x*h)
                ity = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*w)

                mtx = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x*h)
                mty = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y*w)

                rtx = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x*h)
                rty = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y*w)

                ptx = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x*h)
                pty = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y*w)

                # print(thtx, thty, ptx, pty)

                if(distance(itx, ity, thtx, thty) < 10 and abs(prev_off_time - current_time) > 4):
                    print("power of")
                    cv2.putText(image, 'Power Signal', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    curr.execute("INSERT INTO movement (direction, time) VALUES ('power', NOW())")
                    db.commit()
                    prev_off_time = current_time
                elif(distance(mtx, mty, thtx, thty) < 15 and abs(prev_ch_time - current_time) > 2):
                    print("Next Channel")
                    cv2.putText(image, 'Power Signal', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    curr.execute("INSERT INTO movement (direction, time) VALUES ('next_ch', NOW())")
                    db.commit()
                    prev_ch_time = current_time
                elif(distance(rtx, rty, thtx, thty) < 10 and abs(prev_ch_time - current_time) > 2):
                    print("Prev Channel")
                    cv2.putText(image, 'Power Signal', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    curr.execute("INSERT INTO movement (direction, time) VALUES ('prev_ch', NOW())")
                    db.commit()
                    prev_ch_time = current_time
                elif(distance(ptx, pty, thtx, thty) < 10 and abs(prev_mute - current_time) > 2):
                    print("Mute", math.sqrt(abs((ptx - thtx)*2 + (pty - thty)*2)))
                    cv2.putText(image, 'Power Signal', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    curr.execute("INSERT INTO movement (direction, time) VALUES ('mute', NOW())")
                    db.commit()
                    prev_mute = current_time

            elif classificaion.classification[0].label == "Right":
                thtx = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*h)
                thty = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*w)

                itx = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x*h)
                ity = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*w)

                mtx = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x*h)
                mty = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y*w)

                rtx = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x*h)
                rty = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y*w)

                ptx = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x*h)
                pty = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y*w)

                if(distance(itx, ity, thtx, thty) < 10 ):
                    print("Volume Up")
                    cv2.putText(image, 'Power Signal', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    curr.execute("INSERT INTO movement (direction, time) VALUES ('vol_up', NOW())")
                    db.commit()
                    prev_off_time = current_time
                elif(distance(mtx, mty, thtx, thty) < 15 ):
                    print("Volume Down")
                    cv2.putText(image, 'Power Signal', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    curr.execute("INSERT INTO movement (direction, time) VALUES ('vol_down', NOW())")
                    db.commit()
                    prev_ch_time = current_time
            
    # print(X1)

    fps = FPS()
    cv2.putText(image, 'FPS = ' + str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(10) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()

db.close()