# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 15:49:38 2021

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