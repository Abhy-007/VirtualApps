# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 20:00:40 2021

@author: 2014326
"""
import pyrealsense2 as rs
#import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
pipeline.start(config)

while True:
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    
    
    cv2.imshow("depth frame",depth_frame)
    cv2.imshow("Color frame",color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

        
        

