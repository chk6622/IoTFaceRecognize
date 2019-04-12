#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 27, 2018

@author: xingtong
'''

import time
from logger.LogConfig import appLogger
import threading

ser1Lock = threading.Lock()

class PrintTool(object):
    '''
    classdocs
    '''
#     timeMap={}
#     periodMap={}


    def __init__(self):
        '''
        Constructor
        '''
        self.timeMap={}
        self.periodMap={}
        
    def printStartMessage(self,message):
        ser1Lock.acquire()
        sReturn='Beginning: '
        if message:
            timeArray=self.timeMap.get(message)
            if not timeArray:
                timeArray=[]
                self.timeMap[message]= timeArray
            sReturn='Beginning: %-s...' %message
            timeArray.append(self.getCurTime())
        appLogger.info(sReturn)
        ser1Lock.release()
        
    def printEndMessage(self,message):
        ser1Lock.acquire()
        sReturn='Finishing: '
        if message:
            timeArray=self.timeMap.get(message)
            if not timeArray:
                timeArray=[]
            timeArray.append(self.getCurTime())
#             periodArray=self.periodMap.get(message)
            sReturn='Finishing: %-50s spending: %6d ms, max: %6d ms, min: %6d ms, avg: %6d ms' % (message,self.getPeriod(message),max(self.periodMap.get(message)),min(self.periodMap.get(message)),self.getAvg(self.periodMap.get(message)))
        appLogger.info(sReturn)
        ser1Lock.release()
        
    def getCurTime(self):
        return int(round(time.time() * 1000))
    
    def getAvg(self, array):
        avg=0
        total=0
        try:
            if array:
                for item in array:
                    total+=item
                avg=total/len(array)
        except Exception as err:
            appLogger.error(err)
        return avg
    
    def getPeriod(self,message):
        dReturn=0
        try:
            timeArray=self.timeMap.get(message)
            periodArray=self.periodMap.get(message)
            if not periodArray:
                periodArray=[]
                self.periodMap[message]=periodArray
            if timeArray:
                dReturn=timeArray[-1]-timeArray[-2]
                periodArray.append(dReturn)
        except Exception as err:
            appLogger.error(err)
        return dReturn
    
    def getTotalStatistics(self):
        sReturn='The whole procedure:'
        tempMap={}
        for (k,v) in self.periodMap.items():
            if ' - ' in k:
                lastStr=k.split(' - ')[-1]
                tempArray = tempMap.get(lastStr)
                if not tempArray:
                    tempArray=[]
                    tempMap[lastStr]=tempArray
                tempArray.append(self.getAvg(v))
        for (k,v) in tempMap.items():
            sReturn+=' %s : %d ;' % (k,self.getAvg(v))
        appLogger.info(sReturn)
        return sReturn
    
#     def getMaxPeriod(self,message):
#         maxPeriod=0
#         try:
#             timeArray=self.timeMap.get(message)
#             if timeArray:
#                 arraySize=len(timeArray)
#                 for ind in range(0,arraySize,2):
#                     nextInd=ind+1
#                     if nextInd==arraySize:
#                         nextInd=ind
#                     period=timeArray[nextInd]-timeArray[ind]
#                     if period>maxPeriod:
#                         maxPeriod=period
#         except Exception, err:
#             print err
#         return maxPeriod
#     
#     def getMinPeriod(self,message):
#         minPeriod=100000000000000
#         try:
#             timeArray=self.timeMap.get(message)
#             if timeArray:
#                 arraySize=len(timeArray)
#                 for ind in range(0,arraySize,2):
#                     nextInd=ind+1
#                     if nextInd==arraySize:
#                         nextInd=ind
#                     period=timeArray[nextInd]-timeArray[ind]
#                     if period<minPeriod:
#                         minPeriod=period
#         except Exception, err:
#             print err
#         return minPeriod
#     
#     def getMaxPeriod1(self,timeArray):
#         maxPeriod=0
#         try:
#             if timeArray:
#                 arraySize=len(timeArray)
#                 for ind in range(0,arraySize,2):
#                     nextInd=ind+1
#                     if nextInd==arraySize:
#                         nextInd=ind
#                     period=timeArray[nextInd]-timeArray[ind]
#                     if period>maxPeriod:
#                         maxPeriod=period
#         except Exception, err:
#             print err
#         return maxPeriod

if __name__ == '__main__':
#     pt=PrintTool()
#     tA=[1,15,100,120]
#     print pt.getMaxPeriod1(tA)
#     l=[1,2,3,4,5,6]
#     print l[-2:]
    pt=PrintTool()
    pt.printStartMessage('a - abc')
    time.sleep( 1 )
    pt.printStartMessage('b - abcd')
    time.sleep( 2 )
    pt.printEndMessage('b - abcd')
    time.sleep( 1 )
    pt.printEndMessage('a - abc')
    pt.printStartMessage('c - abc')
    time.sleep( 3 )
    pt.printStartMessage('d - abcd')
    time.sleep( 1 )
    pt.printEndMessage('d - abcd')
    time.sleep( 1 )
    pt.printEndMessage('c - abc')
    pt.printStartMessage('abc')
    time.sleep( 1 )
    pt.printStartMessage('abcd')
    time.sleep( 2 )
    pt.printEndMessage('abcd')
    time.sleep( 1 )
    pt.printEndMessage('abc')
    
    pt.getTotalStatistics()
        
        
        
        
        
        