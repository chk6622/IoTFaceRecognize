#!/usr/bin/env python
#coding: utf-8
'''
Created on Apr 09, 2019

@author: xingtong
'''
from baseprocessor.BaseProcessor import BaseProcessor
import cv2
from datetime import datetime
import utiles.Tools as Tools
import os

def get_parent_folder_path():
    return os.path.abspath(os.path.dirname(os.getcwd()))

def get_grand_parent_folder_path():
    return os.path.abspath(os.path.join(os.getcwd(), "../.."))

def get_abs_path(base_path,path_names):
    return os.path.join(base_path,path_names)

folder_path='video'
parent_folder_path=get_parent_folder_path()
output_folder=get_abs_path(parent_folder_path,folder_path)

time1 = datetime.now()
file_name = '%s.avi' % time1.strftime('%Y-%m-%d %H:%M')

output_file=get_abs_path(output_folder,file_name)


class ShowFaceImageProcessor(BaseProcessor):
    '''
    this class is used to show face image
    '''

    def __init__(self,inputQueue=None,outputQueue=None):
        super(ShowFaceImageProcessor,self).__init__(inputQueue=inputQueue,outputQueue=outputQueue)
        self.font = cv2.FONT_HERSHEY_DUPLEX
        self.out = cv2.VideoWriter(output_file, -1, 25.0, (800, 600))

            
    def process(self,processObj=None):
        if processObj is not None:
            frame=processObj.frame
            face_locations=processObj.face_locations
            face_names=processObj.face_names
            frame_info='%s,%s,%s' % (processObj.captured_university, processObj.captured_classroom, Tools.format_date_time(processObj.captured_time,'%Y%m%d%H%M%S','%Y-%m-%d %H:%M:%S'))
            # recoverParam=1
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # top *= recoverParam
                # right *= recoverParam
                # bottom *= recoverParam
                # left *= recoverParam
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), self.font, 1.0, (255, 255, 255), 1)
            cv2.putText(frame, frame_info, (5, 30), self.font, 1.0, (255, 255, 255), 1)
            cv2.namedWindow("Image")
            cv2.imshow("Image", frame)
            self.out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                pass
            #     break
        return processObj

