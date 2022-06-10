# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 23:11:55 2021

@author: 2014326
"""

import cv2
from cvzone.HandTrackingModule import HandDetector
#import cvzone
from pygame import mixer
from time import sleep
import time
import numpy as np
import cvzone
# from pynput.keyboard import Controller
# import os
# import sys
import speech_recognition as sr
listener = sr.Recognizer()

def main():
    
    """ -------- Virtual KB Declarations------"""
    one = False
    three = False
    playsound = True
    click_sound = True
    screen = False
    finger=[]
    
    
    # =============================================================================
    # def function_sound(playsound):
    #     mixer.init()
    #     sound = mixer.Sound('welcome.ogg')
    #     if playsound:
    #         sound.play()
    #         playsound = False
    # =============================================================================
    
    #song = AudioSegment.from_mp3('welcome.mp3')
    cap = cv2.VideoCapture(0)
    
    
    cap.set(3, 1280)
    cap.set(4, 720)
    
    detector = HandDetector(detectionCon=0.8)
    option1 = cv2.imread("1.jpg")
    option2 = cv2.imread("2.jpg")
    option3 = cv2.imread("3.jpg")
    
    keys = [["Q","W","E","R","T","Y","U","I","O","P"],
            ["A","S","D","F","G","H","J","K","L",";"],
            ["Z","X","C","V","B","N","M",",",".","/"," "]]
    finalText = ""
    buttonList = []
    
    
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
    
    def option_screen(img):
        img[40:127,0:500] = option1
        img[180:267,0:500] = option2
        img[320:407,0:500] = option3
        return img
    
    
    
    
    def virtual_key(finalText):
        success,img = cap.read()
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
                    #pTime += cTime
                    #diff = pTime - cTime
                    #pTime = cTime
                    #print(m)
                    
                    if  m < 100:
                        #keyboard.press(button.text)
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
                
               
            cv2.imshow("Welcome",img)
            cv2.waitKey(1)
                
        cv2.rectangle(img,(50,350),(700,450),(175,0,175),cv2.FILLED)
        cv2.putText(img, finalText, (60,425), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255),5)        
                    
        return img
        
    """ ------Virtual Calci Declarations------"""
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
        
        
    # =============================================================================
    #         lmList = []
    #         m=0
    #         hands, img = detector.findHands(img)
    #         if hands:
    #             hand1 = hands[0]
    #             lmList = hand1['lmList']
    #             finger = detector.fingersUp(hand1)
    #         img = drawAll(img, buttonList)
    #         
    #         if lmList:
    #             for button in buttonList:
    #                 x,y = button.pos
    #                 w,h = button.size
    #                 
    #                 if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h:
    #                     cv2.rectangle(img,button.pos,(x+w,y+h),(175,0,175),cv2.FILLED)
    #                     cv2.putText(img, button.text, (x+20,y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255),4)
    #                     m,_,_ = detector.findDistance(lmList[4], lmList[5],img)
    #                 
    #                 if  m < 100:
    #                     #self.keyboard.press(button.text)
    #                     #play(song)
    #                     cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
    #                     cv2.putText(img, button.text, (x+20,y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255),4)
    #                     finalText += button.text
    #                     sleep(0.25)
    #         
    #                 if finger == [1,1,1,0,0]:
    #                     finalText = finalText[:-1]
    #                     sleep(0.25)
    #             
    #                 if finger == [1,1,1,1,1]:
    #                     finalText=""
    #                     
    #         cv2.rectangle(img,(50,350),(700,450),(175,0,175),cv2.FILLED)
    #         cv2.putText(img, finalText, (60,425), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255),5)
    #         return img
    # =============================================================================
    
    def start_page(img):
        img = option_screen(img)
    
    
    
    
    for i in range(len(keys)):
            for j, key in enumerate(keys[i]):
                buttonList.append(Button([100*j+50,100*i+50],key))
    
    
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img)
        
        
        if hands:
            mixer.init()
            hand1 = hands[0]
            finger = detector.fingersUp(hand1)
            sound = mixer.Sound('welcome.ogg')
            if playsound:
                sound.play()
                playsound = False
                screen = True
        
              
        if screen:
            img = option_screen(img)
            
            
            #hand2 = hands[1]
           
            
        if finger ==[0,1,0,0,0]:
            sound1 = mixer.Sound('click.ogg')
            cv2.putText(img, "Loading Virtual KB", (50,500), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255),5)
            if click_sound:
                sound1.play()
                click_sound = False
                one = True
          
        if finger ==[0,1,1,1,0]:
            sound1 = mixer.Sound('click.ogg')
            cv2.putText(img, "Loading Virtual Calci", (50,500), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255),5)
            if click_sound:
                sound1.play()
                click_sound = False
                one = False
                three = True
            
            #img = virtual_key(finalText)
            #exec(open('VirtualKB.py').read())
            
            
            
        cv2.imshow("Welcome",img)
        if cv2.waitKey(1)==27 or finger == [0,1,0,0,0] or finger == [0,1,1,1,0]:
            break
    
    
    if one:  
        cap.release()
        cv2.destroyWindow('Welcome')
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)
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
                        #cTime = time.time()
                        #pTime += cTime
                        #diff = pTime - cTime
                        #pTime = cTime
                        #print(m)
                        
                        if  m < 100:
                            #keyboard.press(button.text)
                            #play(song)
                            sound2 = mixer.Sound('click.ogg')
                            sound2.play()
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
            if cv2.waitKey(1) == 27 or finger==[1,0,0,0,1]:
                cv2.destroyWindow('Virtual KB')
                main()
                break
            
    if three:
        #Webcam
        cap.release()
        cv2.destroyWindow('Welcome')
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
            if cv2.waitKey(1) == 27 or finger==[1,0,0,0,1]:
                cv2.destroyWindow('Virtual Calci')
                main()
                break
        
        
    cap.release()
    cv2.destroyAllWindows()

try:
    with sr.Microphone() as source:
        print('listening')
        voice = listener.listen(source)
        command = listener.recognize_google(voice)
        print(command)
except:
    pass
    

main()