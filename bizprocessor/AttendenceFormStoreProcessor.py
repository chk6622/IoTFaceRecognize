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
            if face_names is not None and len(face_names)>0:
                captured_university=processObj.captured_university
                captured_classroom=processObj.captured_classroom
                captured_time = processObj.captured_time
                for name in face_names:
                    if name == 'Unknown':
                        continue
                    attendence_form.create(university=captured_university,classroom=captured_classroom, datetime=captured_time, student_name=name)
        return processObj