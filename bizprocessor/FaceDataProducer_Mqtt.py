#!/usr/bin/env python
# coding: utf-8
'''
Created on Apr 8, 2019

@author: xingtong
'''

from baseprocessor.BaseProcessor import BaseProcessor
from model.StreamBox import StreamBox
from model.StopSignal import StopSignal
from logger.LogConfig import appLogger
from logger.StreamLogger import StreamLogger
import time, os, cv2, traceback
from datetime import datetime
from socket_tools.connection_tool import connector
from utiles.MqttTool import MqttTool
import numpy as np
from utiles.Tools import *

class FaceDataProducer_Mqtt(BaseProcessor):
    '''
    this class produces data which needs to be processed by streamline
    '''
    productCount = 0

    def __init__(self, inputQueue=None, outputQueue=None):
        super(FaceDataProducer_Mqtt, self).__init__(inputQueue=inputQueue, outputQueue=outputQueue)
        self.mqttTool=MqttTool()

    def process(self, processObj=None):
        streamBox = None
        try:
            topic,data = self.mqttTool.recvDataFromServer()
            if topic is None:
                return None
            streamBox = StreamBox()
            streamBox.captured_university, streamBox.captured_classroom, streamBox.captured_time = topic.split('/')

            if get_frame_time_difference(streamBox.captured_time)>1:
                return None
            image = np.asarray(bytearray(data), dtype="uint8")
            frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
            streamBox.rgb_small_frame=frame[:, :, ::-1]
            streamBox.frame = frame
        except StopIteration:
            return StopSignal()
        except Exception as e:
            appLogger.error(e)
            traceback.print_exc()
            # return None
        return streamBox

    def run(self):
        # self.outputQueue.put(object(),block=True)
        # appLogger.info('init queue...')
        #         time.sleep(20)
        try:
            while self.__class__.isServer:
                beginTime = time.time()
                # print('%s begin execute' % self.__class__)
                processObj = self.process()
                # print('%s finish execute' % self.__class__)
                endTime = time.time()
                if isinstance(processObj, StreamLogger):
                    processObj.setProcessorLog(self.__class__.__name__, beginTime, endTime)
                if processObj is not None and self.outputQueue is not None:
                    if isinstance(processObj, StreamBox):
                        self.__class__.productCount = self.__class__.productCount + 1
                    if isinstance(processObj, StopSignal):
                        processObj.productCount = self.__class__.productCount
                        self.__class__.isServer = False
                        self.mqttTool.close()
                    self.outputQueue.put(processObj, block=True)
                time.sleep(0.01)
        except Exception as e:
            traceback.print_exc()

#                 print 'producer put a box in the queue' 
#             time.sleep(0)
