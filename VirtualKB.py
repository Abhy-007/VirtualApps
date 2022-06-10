# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 07:11:24 2021

@author: 2014326
"""

import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import time
import numpy as np
import cvzone
from pynput.keyboard import Controller
#from playsound import playsound
#from pydub import AudioSegment
#from pydub.playback import play


pTime=0
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
#song = AudioSegment.from_wav('click_s.wav')

detector = HandDetector(detectionCon=0.5)
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"," "]]
finalText = ""
keyboard = Controller()

# =============================================================================
# def drawAll(img,buttonList):
#     
#     for button in buttonList:
#         x,y = button.pos
#         w,h = button.size
#         cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
#         cv2.putText(img, button.text, (x+10,y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255),4)
#     return img
# =============================================================================

def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x,y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0],button.pos[1],button.size[0],button.size[1]),20,rt=0)
        cv2.rectangle(imgNew,button.pos,(x+button.size[0],y+button.size[1]),(255,0,255),cv2.FILLED)
        cv2.putText(imgNew,button.text,(x+40,y+60),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3)
    
    out = img.copy()
    alpha=0.5
    mask=imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1-alpha,0)[mask]
    return out

class Button():
    def __init__(self,pos,text,size=[70,70]):
        self.pos  = pos
        self.size = size
        self.text = text
    


buttonList = []

for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(Button([100*j+50,100*i+50],key))
        





    
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    
    lmList=[]
    
    
    if hands:
        hand1 = hands[0]
        lmList = hand1['lmList']
        finger = detector.fingersUp(hand1)
        
    
    img = drawAll(img, buttonList)
    
    if lmList:
        for button in buttonList:
            x,y = button.pos
            w,h = button.size
            
            if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h:
                cv2.rectangle(img,button.pos,(x+w,y+h),(175,0,175),cv2.FILLED)
                cv2.putText(img, button.text, (x+20,y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255),4)
                
                l,_,_ = detector.findDistance(lmList[8], lmList[12],img)
                m,_,_ = detector.findDistance(lmList[4], lmList[5],img)
                z = lmList[7][2]
                cTime = time.time()
                pTime += cTime
                diff = pTime - cTime
                #pTime = cTime
                #print(m)
                
                if  m < 100:
                    keyboard.press(button.text)
                    #play(song)
                    cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                    cv2.putText(img, button.text, (x+20,y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255),4)
                    finalText += button.text
                    sleep(0.25)
                
                if finger == [1,1,1,0,0]:
                    finalText = finalText[:-1]
                    sleep(0.25)
                
                if finger == [1,1,1,1,1]:
                    finalText=""
            
           
            
    cv2.rectangle(img,(50,350),(700,450),(175,0,175),cv2.FILLED)
    cv2.putText(img, finalText, (60,425), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255),5)        
                
    
    
    cv2.imshow("Virtual KB",img)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
