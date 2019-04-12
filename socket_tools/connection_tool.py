#!/usr/bin/python
#-*-coding:utf-8 -*-


from socket import *
import cv2
import numpy
import traceback
import struct
from multiprocessing.connection import Listener, Client
import os



class connector(object):


    def __init__(self, host = 'localhost', port = 8080):
        self.host=host
        self.port=port
        # self.conn=None
        # self.client=None


    def create_server(self):
        '''
        create server
        '''
        server = Listener((self.host, self.port))
        return server

    def getConn(self, server):
        while True:
            conn = server.accept()
            yield conn

    def create_client(self):
        '''
        connect remote server
        '''

        client = Client((self.host, self.port))
        return client

    # def close_conn(self):
    #     '''
    #     close connect
    #     '''
    #     if self.conn is not None:
    #         self.conn.close()
    #     if self.client is not None:
    #         self.client.close()


    # def recv_data(self,conn):
    #     '''
    #     receive data from remote host
    #     :param:
    #     :return: received data
    #     '''
    #     iReturn=None
    #     try:
    #         if self.conn is not None:
    #             iReturn=self.conn.recv()
    #         # else:
    #         #     iReturn=self.client.recv()
    #     except Exception as e:
    #         traceback.print_exc()
    #     return iReturn


    # def send_data(self, conn, send_data=None):
    #     '''
    #     send data to remote host
    #     :param conn:
    #     :param send_data:
    #     :return:
    #     '''
    #     fReturn=False
    #     try:
    #         if send_data is not None:
    #             if conn is not None:
    #             #     self.client.send(send_data)
    #             # if self.conn is not None:
    #                 conn.send(send_data)
    #             fReturn=True
    #     except Exception as e:
    #         traceback.print_exc()
    #     return False

if __name__=='__main__':
    obj=connector('localhost',8081)
    obj.create_server()
