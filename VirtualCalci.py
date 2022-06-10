# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 11:48:09 2021

@author: 2014326
"""

import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import cvzone

class Button_calci:
    def __init__(self,pos,width,height,value):
        
        self.pos=pos
        self.width = width
        self.height = height
        self.value = value
        
    # def draw(self,img):
        
    #     cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(225,225,225),cv2.FILLED)
    #     cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(50,50,50),3)
    #     cv2.putText(img,self.value,(self.pos[0]+30,self.pos[1]+70),cv2.FONT_HERSHEY_PLAIN,2,(50,50,50))
    
    
    
    def checkClick_calci(self,x,y):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(255,255,255),cv2.FILLED)
            cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(50,50,50),3)
            cv2.putText(img,self.value,(self.pos[0]+20,self.pos[1]+70),cv2.FONT_HERSHEY_PLAIN,5,(0,0,0),5)
            return True
        else:
            return False

    def draw_calci(img,buttonList):
            imgNew = np.zeros_like(img, np.uint8)
            for button in buttonList:
                x,y = button.pos
                cvzone.cornerRect(imgNew, (x,y,button.width,button.height),20,rt=0)
                cv2.rectangle(img,button.pos,(x+button.width,y+button.height),(225,225,225),cv2.FILLED)
                cv2.rectangle(img,button.pos,(x+button.width,y+button.height),(50,50,50),3)
                cv2.putText(img,button.value,(button.pos[0]+30,button.pos[1]+70),cv2.FONT_HERSHEY_PLAIN,2,(50,50,50))
            out = img.copy()
            alpha=0.5
            mask=imgNew.astype(bool)
            out[mask] = cv2.addWeighted(img, alpha, imgNew, 1-alpha,0)[mask]
            return out

#Webcam
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = HandDetector(detectionCon=0.8, maxHands=1)

#Creating Buttons
buttonListvalues = [['7','8','9','*'],
                    ['4','5','6','-'],
                    ['1','2','3','+'],
                    ['/','0','.','=']]




buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x*100 + 800
        ypos = y*100 + 150
        buttonList.append(Button_calci((xpos,ypos),100,100,buttonListvalues[y][x]))
        

#Variables
myEquation = ''
delayCounter = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    
    hands, img = detector.findHands(img, flipType=False)
    
    cv2.rectangle(img,(800,50),(800+400,70+100),(225,225,225),cv2.FILLED)
    cv2.rectangle(img,(800,50),(800+400,70+100),(50,50,50),3)
    
    # for button in buttonList:
    #     button.draw(img)
    img = Button_calci.draw_calci(img,buttonList)
    
    #Check for hands
    if hands:
        lmList = hands[0]['lmList']
        finger = detector.fingersUp(hands[0])
        m,_,_ = detector.findDistance(lmList[4], lmList[5],img)
        x,y,z = lmList[8]
        if m < 100:
            for i,button in enumerate(buttonList):
                if button.checkClick_calci(x, y) and delayCounter == 0:
                    myValue = buttonListvalues[int(i%4)][int(i/4)]
                    if myValue == '=':
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myValue
                    delayCounter = 1
                
        if finger == [1,1,1,0,0]:
            myEquation = myEquation[:-1]
                
            
        if finger == [1,1,1,1,1]:
            myEquation=""
    # Avoiding Duplicates
    if delayCounter !=0:
        delayCounter+=1
        if delayCounter>10:
            delayCounter=0
    
    #Display the equation/result
    cv2.putText(img,myEquation,(810,120),cv2.FONT_HERSHEY_PLAIN,3,(50,50,50),3)
    
    cv2.imshow("Virtual Calci",img)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()