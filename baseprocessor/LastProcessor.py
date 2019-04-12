#!/usr/bin/env python
#coding: utf-8
'''
Created on Apr 09, 2019

@author: xingtong
'''

import sys,time
from baseprocessor.BaseProcessor import BaseProcessor
from model.StopSignal import StopSignal
from logger.StreamLogger import StreamLogger
from logger.LogConfig import appLogger
from model.StreamBox import StreamBox



class LastProcessor(BaseProcessor):
    
    def process(self,processObj):
#         if isinstance(processObj,StreamBox):
#             image=processObj.image
#             if isinstance(image, Image):
#                 processObj.image=image.tobytes()
#                 processObj.size=image.size
#                 processObj.mode=image.mode
#                 del(image)
        return processObj
    
    def run(self):
        while self.__class__.isServer:
            processObj=None
            
            if self.inputQueue:
                processObj=self.inputQueue.get()
                if not processObj:
                    time.sleep(0.01)
                    continue
#             beginTime=time.time()    
            processObj=self.process(processObj=processObj)
#             endTime=time.time()
#             if isinstance(processObj, StreamLogger):
#                 processObj.setProcessorLog(self.__class__.__name__,beginTime,endTime)

#             if processObj and isinstance(processObj,StopSignal):
#                 self.__class__.isServer=False
#                 appLogger.info('%s thread stop' % self.__class__.__name__)          
            
            if processObj and self.outputQueue:
                self.outputQueue.put(processObj)