#!/usr/bin/env python
#coding: utf-8
'''
Created on Apr 09, 2019

@author: xingtong
'''
from baseprocessor.BaseProcessor import BaseProcessor
import cv2
import face_recognition

# def getWebPageSipder(appConfig):
#     mainPageUrl=appConfig.get('WebPageSpider','MAIN_PAGE_URL')
#     cookiePath=appConfig.get('WebPageSpider','COOKIE_PATH')
#     tempDocPath=appConfig.get('WebPageSpider','TEMP_DOC_PATH')
#     return WebPageSpider(mainPageUrl,cookiePath,tempDocPath)

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
            face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=3, model="hog")
            processObj.face_locations=face_locations
        return processObj

