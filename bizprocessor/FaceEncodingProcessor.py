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

class FaceEncodingProcessor(BaseProcessor):
    '''
    this class is used to encode face image
    '''

    def __init__(self,inputQueue=None,outputQueue=None):
        super(FaceEncodingProcessor,self).__init__(inputQueue=inputQueue,outputQueue=outputQueue)
        # self.webSpider=getWebPageSipder(self.appConfig)
            
    def process(self,processObj=None):
        if processObj is not None:
            rgb_small_frame=processObj.rgb_small_frame
            face_locations=processObj.face_locations
            face_encodings = []
            if len(face_locations) > 0:
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations, num_jitters=1)
            processObj.face_encodings=face_encodings
        return processObj

