#!/usr/bin/python
#-*-coding:utf-8 -*-

import multiprocessing
import cv2
import time
from socket_tools.connection_tool import connector
import traceback

class image_send(multiprocessing.Process):
    def __init__(self,inputQueue=None,outputQueue=None):
        multiprocessing.Process.__init__(self)
        self.inputQueue=inputQueue
        self.outputQueue=outputQueue
        remote_port = 8080
        remote_ip = 'localhost'
        self.client = self.connectToRemoteHost(remote_ip,remote_port)
        self.resize = 1  # Resize frame of video  for faster face recognition processing
        self.recoverParam = int(1/self.resize)
        # print('init %s finished' % self.__class__)

    def connectToRemoteHost(self,remote_ip='localhost',remote_port='8080'):
        client=None
        try:
            client=connector(remote_ip,remote_port)
            client.create_client()
        except Exception as e:
            traceback.print_exc()
            client=None
        return client

    def close_client(self):
        if self.client is not None:
            self.client.close_conn()
            self.client=None


    def recognize_face(self, frame):
        lReturn=[]
        small_frame = cv2.resize(frame, (0, 0), fx=self.resize, fy=self.resize)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        self.client.send_data(rgb_small_frame)
        response_msg = self.client.recv_data()
        if response_msg is not None:
            face_locations = response_msg.get('face_locations')
            face_names = response_msg.get('face_names')
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= self.recoverParam
                right *= self.recoverParam
                bottom *= self.recoverParam
                left *= self.recoverParam
                lReturn.append(((top, right, bottom, left, name)))
        return lReturn

    def send_image(self):
        if self.inputQueue is None and self.outputQueue is None:
            return
        while True:
            frame=self.inputQueue.get(block=True)
            if frame is not None:
                respone_msg=self.recognize_face(frame)
            self.outputQueue.put(respone_msg,block=True)
            time.sleep(0.1)

    def run(self):
        self.send_image()
