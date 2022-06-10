#Importing Libraries

import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import time
import numpy as np
import cvzone
from pynput.keyboard import Controller
from pygame import mixer
import pygame


#Class Declaration

class VirtualKB:
   
    def __init__(self):
        self.detector = HandDetector(detectionCon=0.6)
        
        self.keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"," "]]
        
        self.finalText = ""
        
        


#Function for drawing boxes
    def drawAll(self,img):
        buttonList = []

        for i in range(len(self.keys)):
                for j, key in enumerate(self.keys[i]):
                    buttonList.append(Button([100*j+50,100*i+50],key))
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
        return out, buttonList


#Function for Virtual KB operation
    def VirtualKey(self,img,buttonList):
        pygame.mixer.init()
        lmList = []
        hands, img = self.detector.findHands(img)
        delaycounter = 0
        #click_sound = True
        
        if hands:
            hand1 = hands[0]
            lmList = hand1["lmList"]
            finger = self.detector.fingersUp(hand1)
        
        if lmList:
            for button in buttonList:
                x,y = button.pos
                w,h = button.size
                
                if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h:
                    cv2.rectangle(img,button.pos,(x+w,y+h),(175,0,175),cv2.FILLED)
                    cv2.putText(img, button.text, (x+20,y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255),4)
                    
                    
                    m,_,_ = self.detector.findDistance(lmList[4], lmList[5],img)
                    if  m < 100:
                        #keyboard.press(button.text)
                        #play(song)
                        sound2 = mixer.Sound('click.ogg')
                        sound2.play()
                        cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                        cv2.putText(img, button.text, (x+20,y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255),4)
                        self.finalText += button.text
                        sleep(0.25)
                        #delaycounter = 1
                    
                    if finger == [1,1,1,0,0]:
                        self.finalText = self.finalText[:-1]
                        sleep(0.25)
                        #delaycounter = 1
                    
                    if finger == [1,1,1,1,1]:
                        self.finalText=""
                    
                    if delaycounter!=0:
                        delaycounter+=1
                        if delaycounter>30:
                            delaycounter = 0
        


        cv2.rectangle(img,(50,350),(700,450),(175,0,175),cv2.FILLED)
        cv2.putText(img, self.finalText, (60,425), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255),5) 

        return img



#Another class for buttons
class Button():
    def __init__(self,pos,text,size=[70,70]):
        self.pos  = pos
        self.size = size
        self.text = text
        

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)
    
    keyboard = VirtualKB()
    
    while True:
        success, img = cap.read()
        img = cv2.flip(img,1)
        img,buttonList = keyboard.drawAll(img)
        img = keyboard.VirtualKey(img,buttonList)
        
        cv2.imshow("Virtual KB",img)
        if cv2.waitKey(1) == 27:
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
