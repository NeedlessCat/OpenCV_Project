"""
TASK --> to alter the volume corresponding to the distance between the forefinger and the thumb tips.

THINGS WE NEEDED FOR THIS PROJECT
1. Capture the live image --> openCV library
2. detect hand | find the position of both the tips --> mediapipe lib
3. find distance between the two tips --> math lib
4. alter the volume corresponding to the distance --> pycaw lib
5. print sound bar on screen
6. print volume percentage on screen
"""
import cv2
import mediapipe as mp
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# print(volume.GetMute())
# print(volume.GetMasterVolumeLevel())
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
# volume.SetMasterVolumeLevel(-20.0, None)

mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands
hands = mpHands.Hands()

cap = cv2.VideoCapture(0)
while True:
    success,img = cap.read()
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for id,lm in enumerate(handLms.landmark):
                h,w,c = img.shape
                #print(id,lm)
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id,cx,cy])
                #print(lmList)
            # mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
            if lmList:
                x1,y1 = lmList[4][1], lmList[4][2]
                x2,y2 = lmList[8][1], lmList[8][2]
                cv2.circle(img,(x1,y1),15,(1,12,12),cv2.FILLED)
                cv2.circle(img,(x2,y2),15,(1,12,12),cv2.FILLED)
                cv2.line(img,(x1,y1),(x2,y2),(1,12,12),3)
                length = math.hypot(x2-x1,y2-y1)
                # print(length)
                vol = np.interp(length,[50,300],[minVol,maxVol])
                volume.SetMasterVolumeLevel(vol, None)
                
                volBar = np.interp(length , [50 ,300] , [400 ,150])
                volPer = np.interp(length , [50 ,300] , [0 ,100])
                cv2.rectangle(img , (50 ,150) , (85 , 400) ,(123,213,122) ,3)
                cv2.rectangle(img , (50 , int(volBar)) , (85 ,400) ,(0, 231,23) ,cv2.FILLED)
                cv2.putText(img , str(int(volPer)) , (40, 450) ,cv2.FONT_HERSHEY_PLAIN ,4 , (24,34,34) , 3)
            
    cv2.imshow("Image",img)
    cv2.waitKey(1)
    
# length = 50 to 300
# volRange = -63.5 to 0.0
