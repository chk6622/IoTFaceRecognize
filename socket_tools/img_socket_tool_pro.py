#!/usr/bin/python
#-*-coding:utf-8 -*-


from socket import *
import cv2
import numpy
import traceback
import struct
from multiprocessing.connection import Listener, Client
import os



class img_socket_tool(object):


    def __init__(self, host = 'localhost', port = 80):
        self.host=host
        self.port=port
        self.conn=None
        self.client=None


    def create_server(self):
        '''
        create server
        '''
        server = Listener((self.host, self.port))
        self.conn = server.accept()

    def create_client(self):
        '''
        connect remote server
        '''

        self.client = Client((self.host, self.port))

    def close_conn(self):
        '''
        close connect
        '''
        if self.conn is not None:
            self.conn.close()
        if self.client is not None:
            self.client.close()


    def recv_data(self):
        '''
        receive data from remote host
        :param:
        :return: received data
        '''
        iReturn=None
        try:
            if self.conn is not None:
                iReturn=self.conn.recv()
            else:
                iReturn=self.client.recv()
        except Exception as e:
            traceback.print_exc()
        return iReturn


    def send_data(self, send_data=None):
        '''
        send data to remote host
        :param send_data:
        :return:
        '''
        fReturn=False
        try:
            if send_data is not None:
                if self.client is not None:
                    self.client.send(send_data)
                if self.conn is not None:
                    self.conn.send(send_data)
                fReturn=True
        except Exception as e:
            traceback.print_exc()
        return False
