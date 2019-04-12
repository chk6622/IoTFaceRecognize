#!/usr/bin/env python
#coding: utf-8
'''
Created on Apr 12, 2019

@author: xingtong
'''
from baseprocessor.BaseProcessor import BaseProcessor
from model.AttendanceForm import attendence_form

class AttendenceFormStoreProcessor(BaseProcessor):
    '''
    this class is used to store attendence form
    '''

    def __init__(self, inputQueue=None, outputQueue=None):
        super(AttendenceFormStoreProcessor, self).__init__(inputQueue=inputQueue, outputQueue=outputQueue)
        # self.webSpider=getWebPageSipder(self.appConfig)

    def process(self, processObj=None):
        if processObj is not None:
            face_names = processObj.face_names
            captured_location=processObj.captured_location
            captured_time = processObj.captured_time
            for name in face_names:
                attendence_form.create(location=captured_location, datetime=captured_time, student_name=name)
        return processObj