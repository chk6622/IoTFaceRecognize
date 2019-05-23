#!/usr/bin/env python
#coding: utf-8
'''
Created on Apr 09, 2019

@author: xingtong
'''
from baseprocessor.BaseProcessor import BaseProcessor
import cv2
import face_recognition
from utiles.Tools import *


class FaceCapturingProcessor(BaseProcessor):
    '''
    this class is used to show face image
    '''

    def __init__(self,inputQueue=None,outputQueue=None):
        super(FaceCapturingProcessor,self).__init__(inputQueue=inputQueue,outputQueue=outputQueue)
        self.face_locations = None
        self.flag = True
            
    def process(self,processObj = None):
        if processObj is not None:
            rgb_small_frame = processObj.rgb_small_frame
            # if get_frame_time_difference(processObj.captured_time)<=2:
            if self.flag:
                self.face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=2, model="hog")
                self.flag = False
            else:
                self.flag = True
            processObj.face_locations = self.face_locations
        return processObj

