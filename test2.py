# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 00:19:09 2021

@author: 2014326
"""

#import cvzone
import cv2
#from cvzone.HandTrackingModule import HandDetector
from VirtualKey import VirtualKB
import speech_recognition as sr
from pygame import mixer
import pygame
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import pyttsx3
listener = sr.Recognizer()
engine = pyttsx3.init()
option1 = cv2.imread("1.jpg")
option2 = cv2.imread("2.jpg")
option3 = cv2.imread("3.jpg")
keyboard = VirtualKB()
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
pygame.mixer.init()  
detector = HandDetector(detectionCon=0.8)
playsound=True
click_sound = True
one = False
screen = False
finger=[]    
    
    
    
   
def keyboard_draw(img):
    img,buttonList = keyboard.drawAll(img)
    img = keyboard.VirtualKey(img,buttonList)
    return img
    
def option_screen(img):
    img[40:127,0:500] = option1
    sleep(0.1)
    img[180:267,0:500] = option2
    img[320:407,0:500] = option3
    return img    


    
try:
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=1)
        print('listening..')
        voice = listener.listen(source)
        command = listener.recognize_google(voice)
        command= command.lower()
        print(command)
except Exception:
        print("Did not catch that")
       
if "jarvis" in command:
        sound2 = mixer.Sound('welcome.ogg')
        sound2.play()  



    
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    
    hands, img = detector.findHands(img)
    
    if hands:
        mixer.init()
        hand1 = hands[0]
        finger = detector.fingersUp(hand1)
        sound = mixer.Sound('importing.ogg')
        if playsound:
            sound.play()
            playsound = False
            screen = True

      
    if screen:
        img = option_screen(img)
    
    if finger ==[0,1,0,0,0]:
        sound1 = mixer.Sound('click.ogg')
        cv2.putText(img, "Loading Virtual KB", (50,500), cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255),5)
        if click_sound:
            sound1.play()
            click_sound = False
            one = True
            
        

    cv2.imshow("Welcome",img)
        
    if cv2.waitKey(1)==27 or finger == [0,1,0,0,0]:
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
        hands = detector.findHands(img,draw=False)
        img = keyboard_draw(img)
        if hands:
            finger = detector.fingersUp(hands[0])
        
        cv2.imshow("Virtual KB",img)
        if cv2.waitKey(1) == 27 or finger==[1,0,0,0,1]:
            cv2.destroyWindow('Virtual KB')
            
            break
    
    
cap.release()
cv2.destroyAllWindows()





        



