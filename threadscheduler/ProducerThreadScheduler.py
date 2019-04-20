#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 30, 2018

@author: xingtong
'''
import sys,time
from queue import Queue
from logger.LogConfig import appLogger
from baseprocessor.LastProcessor import LastProcessor
from baseprocessor.BaseProcessor import BaseProcessor
import bizprocessor.FaceDataProducer_Mqtt


class ProducerThreadScheduler(object):
    def __init__(self,streamLineTemplate,outputQueue):
        self.streamLineTemplate=streamLineTemplate
        self.outputQueue=outputQueue
       
        
    def CreateSteamLine(self):
        '''
       create a streamline
        @return: a list which contains all bizprocessors(business processors) 
        '''
        streamLineArray=[]
        if self.streamLineTemplate:
            queueSize=self.streamLineTemplate.get('QueueSize')
            p=self.streamLineTemplate.get('Thread')
            outputQueue=None
            if p:
                tCount=p[-1]
                module=sys.modules[p[0]]  
                pClass=getattr(module,p[1])  
                outputQueue=Queue(maxsize=queueSize)
                for i in range(tCount):
                    pObj=pClass(outputQueue=outputQueue) 
                    pObj.domean=True
                    streamLineArray.append(pObj)
            for i in range(1):
                lastProcessor=LastProcessor(inputQueue=outputQueue,outputQueue=self.outputQueue)
                streamLineArray.append(lastProcessor)  #add the last processor
        return streamLineArray
    
    def execute(self):
        '''
        the main function to execute software
        '''
        #create streamline
        streamLineArray=self.CreateSteamLine()
        #start every bizprocessor
        for index,item in enumerate(streamLineArray):
            if isinstance(item,BaseProcessor):
                item.start()
        while True:
            time.sleep(0.1)
        appLogger.info('%s thread stop' % self.__class__.__name__)           