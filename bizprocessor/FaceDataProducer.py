#!/usr/bin/env python
#coding: utf-8
'''
Created on Apr 8, 2019

@author: xingtong
'''

from baseprocessor.BaseProcessor import BaseProcessor
from model.StreamBox import StreamBox
from model.StopSignal import StopSignal
from logger.LogConfig import appLogger
from logger.StreamLogger import StreamLogger
import time,os,cv2,traceback
from datetime import datetime
from socket_tools.connection_tool import connector

# def getApiSpider(appConfig):
#     apiKey=appConfig.get('ApiSpider','API_KEY')
#     queryReturnMaxResult=appConfig.getint('ApiSpider','QUERY_RETURN_MAX_RESULTS')
#     maxQueryCountLimit=appConfig.getint('ApiSpider','MAX_QUERY_COUNT_LIMIT')
#     queryBeginYear=appConfig.get('ApiSpider','QUERY_BEGIN_YEAR')
#     queryEndYear=appConfig.get('ApiSpider','QUERY_END_YEAR')
#     return IeeeApiSpider(apiKey,queryReturnMaxResult,maxQueryCountLimit,queryBeginYear,queryEndYear)

# def getKeywords(appConfig):
#     aReturn=None
#     keyWords=appConfig.get('KayWords','KEY_WORDS')
#     if keyWords:
#         aReturn=keyWords.split(',')
#     return aReturn

class FaceDataProducer(BaseProcessor):
    '''
    this class produces data which needs to be processed by streamline
    '''
    productCount=0
    
    def __init__(self,inputQueue=None,outputQueue=None, host = 'localhost', port = 8080):
        super(FaceDataProducer,self).__init__(inputQueue=inputQueue,outputQueue=outputQueue)
        # self.server = connector(host, port).create_server()
        # self.apiSpider=getApiSpider(self.appConfig)
        # self.generater=self.getResultData()
            
    def process(self,processObj=None):
        streamBox=None
        try:
            conn=self.getConnFromRemote()
            imageMsg = conn.recv()
            streamBox = StreamBox()
            streamBox.captured_time, streamBox.captured_location, streamBox.rgb_small_frame = imageMsg
            streamBox.conn = conn
            # print(streamBox)
            # streamBox.rgb_small_frame, streamBox.frame, streamBox.captured_location, streamBox.captured_time = next(self.generater)
            # return streamBox
        except StopIteration:
            return StopSignal()
        except Exception as e:
            appLogger.error(e)
            traceback.print_exc()
            # return None
        return streamBox


    def getResultDataFromlocalhost(self):
        upper_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
        video_path = os.path.join(upper_dir, 'video', 'test_3.mp4')
        capture = cv2.VideoCapture(0)
        iFrame=0
        # capture.set(cv2.CAP_PROP_POS_FRAMES, iFrame)
        captured_location='wz313'
        while True:
            captured_time = (datetime.now()).strftime('%Y%m%d%H%M%S')
            ret, frame=capture.read()
            # iFrame += 11
            # capture.set(cv2.CAP_PROP_POS_FRAMES, iFrame)
            #     break
            # if not ret:
            #     break
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            yield rgb_small_frame,frame,captured_location,captured_time

    def getConnFromRemote(self):
            conn = self.server.accept()
            return conn

    def get_video_info(self,cap):
        '''
        get the video information
        @return: video information
        '''
        video_info = {
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'num_of_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT))}
        return video_info


            
        
    def run(self):
        # self.outputQueue.put(object(),block=True)
        # appLogger.info('init queue...')
#         time.sleep(20)
        try:
            while self.__class__.isServer:
                beginTime=time.time()
                print('%s begin execute' % self.__class__)
                processObj=self.process()
                print('%s finish execute' % self.__class__)
                endTime=time.time()
                if isinstance(processObj, StreamLogger):
                    processObj.setProcessorLog(self.__class__.__name__,beginTime,endTime)
                if processObj is not None and self.outputQueue is not None:
                    if isinstance(processObj,StreamBox):
                        self.__class__.productCount=self.__class__.productCount+1
                    if isinstance(processObj,StopSignal):
                        processObj.productCount=self.__class__.productCount
                        self.__class__.isServer=False
                    self.outputQueue.put(processObj,block=True)
        except Exception as e:
            traceback.print_exc()
                
#                 print 'producer put a box in the queue' 
#             time.sleep(0)
