# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 13:31:14 2021

@author: 2014326
"""

#Importing necessary Libraries
import cv2
import mediapipe as mp
import time



cap = cv2.VideoCapture(0)
x = cap. get(cv2. CAP_PROP_FRAME_WIDTH )
y = cap. get(cv2. CAP_PROP_FRAME_HEIGHT )

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0
ratio_n = 0.0

print(x,y)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            #print(handLms.landmark)
            xList = []
            yList = []
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                h,w,c = img.shape
                cx,cy,z = int(lm.x*w), int(lm.y*h),(lm.z*100)
                xList.append(cx)
                yList.append(cy)
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                
                if id ==8:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
                    cv2.rectangle(img, (cx-10, cy-10), (cx+10, cy+10), (255,0,0), 2)
                    bbox_n = boxH
                    ratio = (boxW/boxH)*100
                    diff = ratio - ratio_n
                    ratio_n = ratio
                    print(diff)
                
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  (255, 0, 255), 2)
            
    
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)