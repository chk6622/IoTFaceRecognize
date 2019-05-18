#!/usr/bin/env python
#coding: utf-8
'''
Created on Apr 09, 2019

@author: xingtong
'''
import sys,os,time
# project_dir=os.path.dirname(os.path.dirname(__file__))
# print project_dir
# sys.path.append(project_dir)
from logger.LogConfig import appLogger
from processscheduler.ProcessScheduler import ProcessScheduler
# reload(sys)
# sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
#     for module in sys.modules:
#         print module
#     print sys.modules['processscheduler.threadscheduler']
#     print sys.modules['logger.StreamLogger']
    streamLineTemplate=[]
    processQueueSize=50
    streamLineTemplate.append({'QueueSize':50,'pCount':1,'Thread':['bizprocessor.FaceDataProducer_Mqtt','FaceDataProducer_Mqtt',1]})
    streamLineTemplate.append({'QueueSize':50,'pCount':1,'Thread':[
                                                                ['bizprocessor.FaceCapturingProcessor','FaceCapturingProcessor',1]
                                                                   ]})
    streamLineTemplate.append({'QueueSize':50,'pCount':1,'Thread':[['bizprocessor.FaceEncodingProcessor','FaceEncodingProcessor',1]]})
    streamLineTemplate.append({'QueueSize': 50, 'pCount': 1, 'Thread':[
                                                                    # ['bizprocessor.FaceEncodingProcessor','FaceEncodingProcessor',1]
                                                                    ['bizprocessor.FaceComparingProcessor', 'FaceComparingProcessor', 1]
                                                                    ,['bizprocessor.AttendenceFormStoreProcessor', 'AttendenceFormStoreProcessor', 1]
                                                                    # ,['bizprocessor.ReturnRecognitionResultProcessor', 'ReturnRecognitionResultProcessor', 1]
                                                                    ,['bizprocessor.ShowFaceImageProcessor','ShowFaceImageProcessor',1]
                                                                    ]})
 
     
    processScheduler=ProcessScheduler(streamLineTemplate,processQueueSize)
    processScheduler.execute()