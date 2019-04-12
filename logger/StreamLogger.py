#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 29, 2018

XingTong
'''
import sys,time




class StreamLogger(object):
    
    def __init__(self):
        self.processorList=[]  #processor list
        self.startTime=time.time()  #processor's start time
    
    def setProcessorLog(self,clazz,beginTime,endTime):
        '''
        record processor log
        @param clazz:the class of processor
        @param beginTime:the begin time of processor 
        @param endTime:the end time of processor  
        '''
        if self.processorList: #data waiting time
            beforeProcessor=self.processorList[-1] #get before processor
            clazzMid='   %s-%s' % (beforeProcessor[0],clazz)
            midBeginTime=beforeProcessor[2]
            midEndTime=beginTime
            self.processorList.append((clazzMid,midBeginTime,midEndTime))
        self.processorList.append((clazz,beginTime,endTime))
        
    def getTotalPod(self):
        '''
        get the pipeline spends total time to process data  
        '''
        beginTime=endTime=0
        if self.processorList:
            beginTime=self.processorList[0][1]
            endTime=self.processorList[-1][2]
#         print '%f-%f=%f:%s' % (endTime,beginTime,(endTime-beginTime),self.processorList)
        return endTime-beginTime