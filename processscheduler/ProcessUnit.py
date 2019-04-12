#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 30, 2018

@author: xingtong
'''
import sys
from threadscheduler.ConsumerThreadScheduler import ConsumerThreadScheduler
from threadscheduler.ProducerThreadScheduler import ProducerThreadScheduler
import multiprocessing


class ProcessUnit(multiprocessing.Process):
    '''
    the class represent a process
    '''
    def __init__(self,streamLineTemplate,inputQueue=None,outputQueue=None):
        '''
        @param streamLineTemplate: the template of streamline
        @param inputQueue: input queue
        @param outputQueue: output queue
        '''
        multiprocessing.Process.__init__(self)
        self.inputQueue=inputQueue
        self.outputQueue=outputQueue
        self.baseThreadScheduler=None   #thread scheduler
        if not inputQueue:  #if input queue is None then create producer, else create consumer
            self.baseThreadScheduler=ProducerThreadScheduler(streamLineTemplate,outputQueue=self.outputQueue)
        else:
            self.baseThreadScheduler=ConsumerThreadScheduler(streamLineTemplate,inputQueue=self.inputQueue,outputQueue=self.outputQueue)
        
        
    def run(self):
        self.baseThreadScheduler.execute()