#!/usr/bin/env python
#coding: utf-8
'''
Created on Apr 09, 2019

@author: xingtong
'''
import sys,time
from threading import Thread
from logger.StreamLogger import StreamLogger
from model.StopSignal import StopSignal
from logger.LogConfig import appLogger
from configparser import ConfigParser
from model.StreamBox import StreamBox
import traceback

def getConfig():
    configFilePath='../config.conf'
    cf = ConfigParser()
    cf.read(configFilePath)
    return cf

class BaseProcessor(Thread):
    
    isServer=True
    
    def __init__(self,inputQueue=None,outputQueue=None):
        Thread.__init__(self)
        self.inputQueue=inputQueue
        self.outputQueue=outputQueue
        self.appConfig=getConfig()
        

    def process(self,processObj=None):
        print('father')
        if processObj:
            pass
    
    def run(self):
        while self.__class__.isServer:
            processObj=None
            
            if self.inputQueue is not None:
                processObj=self.inputQueue.get(block=True)
                if processObj is None:
                    time.sleep(0.01)
                    continue
            beginTime=time.time()
            try:
                if processObj and isinstance(processObj,StreamBox):
                    # print('%s begin execute' % self.__class__)
                    processObj=self.process(processObj=processObj)
                    # print('%s finish execute' % self.__class__)
            except Exception as e:
                appLogger.error(e)
                traceback.print_stack()
                if processObj:
                    processObj.isError=True
            endTime=time.time()
            if processObj and isinstance(processObj, StreamLogger):
                processObj.setProcessorLog(self.__class__.__name__,beginTime,endTime)

#             if processObj and isinstance(processObj,StopSignal):
#                 self.__class__.isServer=False
#                 appLogger.info('%s thread stop' % self.__class__.__name__)          
            try:
                if processObj is not None and self.outputQueue is not None:
                    self.outputQueue.put(processObj,block=True)
            except Exception as e:
                traceback.print_exc()
            