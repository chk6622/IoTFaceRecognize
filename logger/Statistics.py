#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 30, 2018

@author: xingtong
'''
import sys,time
from logger.StreamLogger import StreamLogger



class Statistics(object):
    
    def __init__(self):
        self.startTime=time.time()  #stream line start time
        self.totalTime=0
        self.totalCount=0  #sys processes total data
        self.totalPod=0  #sys runs total time
        self.totalAvg=0  #total avg processes speed /s
        self.singlePod=0 #sys processing single data spends time
        
        self.processorList=[]
        self.processorTimeDic={}
        
    def addProcessorLog(self,streamLogger):
        if streamLogger and isinstance(streamLogger, StreamLogger):
            if not self.totalCount:
                self.startTime=time.time()
            self.totalCount+=1  #sys processes total data adds 1
            self.totalPod=time.time()-self.startTime  #get sys runs total time
            if not self.totalPod:
                self.totalPod=1
            self.totalAvg=self.totalCount/self.totalPod  #get sys avg speed
            self.singlePod=streamLogger.getTotalPod()
#             print self.singlePod
            
#             print streamLogger.processorList
            for (clazz,beginTime,endTime) in streamLogger.processorList:
                
                if clazz not in self.processorList:
                    self.processorList.append(clazz)  #add processor class into processor list
                statList=self.processorTimeDic.get(clazz)
                if not statList:
                    statList=[]
                    self.processorTimeDic[clazz]=statList
                pod=endTime-beginTime  #get each processor spending time
                if statList:
                    totalPod=pod+statList[1]  #get processor total spending time
                    avgPod=totalPod/self.totalCount  #processor avg spending time
                    maxPod=statList[2]   #highest spending time
                    if pod>maxPod:
                        maxPod=pod
                    minPod=statList[3]  #lowest spending time
                    if pod<minPod:
                        minPod=pod
                    statList=[]
                    self.processorTimeDic[clazz]=statList
                    statList.append(pod)    #current spending time
                    statList.append(totalPod) 
                    statList.append(maxPod)
                    statList.append(minPod) 
                    statList.append(avgPod)  
                else:
                    avgPod=totalPod=maxPod=minPod=pod   
                    statList.append(pod)
                    statList.append(totalPod)
                    statList.append(maxPod)
                    statList.append(minPod)
                    statList.append(avgPod)
#                 print '%s,%s,%s,%s' % (clazz,pod,totalPod,avgPod)
#                 statList.append(endTime)
#                 statList.append(beginTime)
                
                
                
    def getStatisticInfo(self):
        sReturn='start time:%s,total spending time:%.2f s,processing total data:%s,avg processing speed:%.2f /s,the spending time processing single data :%.3f s\n' % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self.startTime)),self.totalPod,self.totalCount,self.totalAvg,self.singlePod)
        for key in self.processorList:
            statList=self.processorTimeDic.get(key)
            sReturn+='%-50s:current spending time%8.3fs；max spending time%8.3fs；min spending time%8.3fs；avg spending time%8.3fs\n' % (key,statList[0],statList[2],statList[3],statList[4])
        return sReturn
                