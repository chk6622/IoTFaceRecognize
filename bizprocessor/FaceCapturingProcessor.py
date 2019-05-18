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
        # self.webSpider=getWebPageSipder(self.appConfig)
            
    def process(self,processObj=None):
        if processObj is not None:
            rgb_small_frame=processObj.rgb_small_frame
            if get_frame_time_difference(processObj.captured_time)<=3:
                face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=2, model="hog")
                processObj.face_locations=face_locations
            else:
                processObj.face_locations = None
        return processObj

