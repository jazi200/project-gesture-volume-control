import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np


cap = cv2.VideoCapture(0)


mpH = mp.solutions.hands
hands = mpH.Hands()
mpD = mp.solutions.drawing_utils

# ностоящий времядагы звукты шығарады
audi = AudioUtilities.GetSpeakers()

interface = audi.Activate( IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


volMin, volMax = volume.GetVolumeRange()[:2]


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    List = []
    if results.multi_hand_landmarks:
        for handlandmark in results.multi_hand_landmarks:
            for id,lm in enumerate(handlandmark.landmark):
                h,w,_ = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                List.append([id,cx,cy])
            mpD.draw_landmarks(img, handlandmark, mpH.HAND_CONNECTIONS)
        
    if List != []:
        x1,y1 = List[4][1], List[4][2]
        x2,y2 = List[8][1], List[8][2]
        
        cv2.circle(img,(x1,y1),6,(0,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),6,(0,0,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),5)
 
        length = hypot(x2-x1,y2-y1)

        vol = np.interp(length,[15,220],[volMin,volMax])
        print(vol,length)
        volume.SetMasterVolumeLevel(vol, None)

    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break

   