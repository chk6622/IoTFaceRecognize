#!/usr/bin/python
#-*-coding:utf-8 -*-

import multiprocessing
import cv2
import time
from datetime import datetime
from socket_tools.connection_tool import connector
import traceback

class image_send(multiprocessing.Process):
    def __init__(self,inputQueue=None,outputQueue=None,location='WZ313'):
        multiprocessing.Process.__init__(self)
        self.inputQueue=inputQueue
        self.outputQueue=outputQueue
        self.remote_port = 8080
        self.remote_ip = 'localhost'

        self.resize = 1  # Resize frame of video  for faster face recognition processing
        self.recoverParam = int(1/self.resize)
        self.location=location
        # print('init %s finished' % self.__class__)

    def connectToRemoteHost(self,remote_ip='localhost',remote_port='8080'):
        client=None
        try:
            conn=connector(remote_ip,remote_port)
            client=conn.create_client()
        except Exception as e:
            traceback.print_exc()
            client=None
        return client

    # def close_client(self):
    #     if self.client is not None:
    #         self.client.close()
    #         self.client=None


    def recognize_face(self, frame):
        if frame is None:
            return
        client = self.connectToRemoteHost(self.remote_ip, self.remote_port)
        if client is None:
            return
        lReturn=[]
        small_frame = cv2.resize(frame, (0, 0), fx=self.resize, fy=self.resize)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        capture_time = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        send_msg=(capture_time,self.location,rgb_small_frame)
        client.send(send_msg)

        while True:
            response_msg = client.recv()
            if response_msg is not None:
                face_locations = response_msg.get('face_locations')
                face_names = response_msg.get('face_names')
                captured_location = response_msg.get('captured_location')
                captured_time = response_msg.get('captured_time')
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    top *= self.recoverParam
                    right *= self.recoverParam
                    bottom *= self.recoverParam
                    left *= self.recoverParam
                    lReturn.append((captured_location, captured_time, top, right, bottom, left, name))
                # client.close()
                break
            else:
                time.sleep(0.01)
        return lReturn

    def send_image(self):
        if self.inputQueue is None and self.outputQueue is None:
            return
        while True:
            frame=self.inputQueue.get(block=True)
            if frame is not None:
                respone_msg=self.recognize_face(frame)
                self.outputQueue.put(respone_msg,block=True)

    def run(self):
        self.send_image()
