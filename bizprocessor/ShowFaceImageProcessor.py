#!/usr/bin/env python
#coding: utf-8
'''
Created on Apr 09, 2019

@author: xingtong
'''
from baseprocessor.BaseProcessor import BaseProcessor
import cv2
import numpy as np

# def getWebPageSipder(appConfig):
#     mainPageUrl=appConfig.get('WebPageSpider','MAIN_PAGE_URL')
#     cookiePath=appConfig.get('WebPageSpider','COOKIE_PATH')
#     tempDocPath=appConfig.get('WebPageSpider','TEMP_DOC_PATH')
#     return WebPageSpider(mainPageUrl,cookiePath,tempDocPath)

class ShowFaceImageProcessor(BaseProcessor):
    '''
    this class is used to show face image
    '''

    def __init__(self,inputQueue=None,outputQueue=None):
        super(ShowFaceImageProcessor,self).__init__(inputQueue=inputQueue,outputQueue=outputQueue)
        # self.webSpider=getWebPageSipder(self.appConfig)
            
    def process(self,processObj=None):
        if processObj is not None:
            # realPdfUrl=processObj.realPdfUrl
            frame=processObj.frame
            rgb_small_frame=processObj.rgb_small_frame
            face_locations=processObj.face_locations
            face_names=processObj.face_names
            recoverParam=4
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= recoverParam
                right *= recoverParam
                bottom *= recoverParam
                left *= recoverParam
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # print(result)
            cv2.namedWindow("Image")
            cv2.imshow("Image", np.hstack([frame, frame]))
            # cv2.waitKey(0)
            # cv2.imshow("Image", frame)
            # cv2.waitKey(0)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                pass
            #     break
        return processObj

