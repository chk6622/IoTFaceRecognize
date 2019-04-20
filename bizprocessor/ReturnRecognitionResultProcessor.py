#!/usr/bin/env python
#coding: utf-8
'''
Created on Apr 12, 2019

@author: xingtong
'''
from baseprocessor.BaseProcessor import BaseProcessor
import time

class ReturnRecognitionResultProcessor(BaseProcessor):
    '''
    this class is used to return result
    '''

    def __init__(self, inputQueue=None, outputQueue=None):
        super(ReturnRecognitionResultProcessor, self).__init__(inputQueue=inputQueue, outputQueue=outputQueue)
        # self.webSpider=getWebPageSipder(self.appConfig)

    def process(self, processObj=None):
        if processObj is not None:
            face_names = processObj.face_names
            face_locations = processObj.face_locations
            myConn=processObj.conn
            response_msg={}
            response_msg['face_names']=face_names
            response_msg['face_locations']=face_locations
            if myConn is not None:
                myConn.send(response_msg)
                # time.sleep(0.05)
                # print(myConn)
                # myConn.close()
        return processObj