#!/usr/bin/python
#-*-coding:utf-8 -*-


from socket import *
import cv2
import numpy
import traceback
import struct
import os

SEND_BUF_SIZE = 1024*10
RECV_BUF_SIZE = 1024*10

class img_socket_tool(object):


    def __init__(self, ip = '', port = 80):
        self.address = (ip,port)
        self.img_socket = socket(AF_INET, SOCK_STREAM)
        bufsize = self.img_socket.getsockopt(SOL_SOCKET, SO_SNDBUF)
        print("Send Buffer size [Before] :%d" % bufsize)
        rcvsize = self.img_socket.getsockopt(SOL_SOCKET, SO_RCVBUF)
        print("Rcv Buffer size [Before] :%d" % rcvsize)


    def create_server(self):
        '''
        create server
        '''
        self.img_socket.setsockopt(
            SOL_SOCKET,
            SO_SNDBUF,
            SEND_BUF_SIZE
        )
        self.img_socket.setsockopt(
            SOL_SOCKET,
            SO_RCVBUF,
            RECV_BUF_SIZE
        )
        bufsize = self.img_socket.getsockopt(SOL_SOCKET, SO_SNDBUF)
        print("Send Buffer size [After] :%d" % bufsize)
        rcvsize = self.img_socket.getsockopt(SOL_SOCKET, SO_RCVBUF)
        print("Rcv Buffer size [After] :%d" % rcvsize)
        self.img_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.img_socket.bind(self.address)
        self.img_socket.listen(True)
        self.conn, self.addr = self.img_socket.accept()

    def connect_server(self):
        '''
        connect remote server
        '''
        self.img_socket.setsockopt(
            SOL_SOCKET,
            SO_SNDBUF,
            SEND_BUF_SIZE
        )
        self.img_socket.setsockopt(
            SOL_SOCKET,
            SO_RCVBUF,
            RECV_BUF_SIZE
        )
        bufsize = self.img_socket.getsockopt(SOL_SOCKET, SO_SNDBUF)
        print("Send Buffer size [After] :%d" % bufsize)
        rcvsize = self.img_socket.getsockopt(SOL_SOCKET, SO_RCVBUF)
        print("Rcv Buffer size [After] :%d" % rcvsize)
        self.img_socket.connect(self.address)

    def close_conn(self):
        '''
        close connect
        '''
        if self.img_socket:
            self.img_socket.close()
        self.img_socket=None

    def recv_size(self):
        filesize=0
        fileinfo_size = struct.calcsize('128sl')
        try:
            buf = self.conn.recv(fileinfo_size)
            if buf:
                filename,filesize = struct.unpack('128sl', buf)
        except Exception as e:
            self.close_conn()
        return filesize
        # buf = b''
        # try:
        #     while count:
        #         tmp_buf = self.conn.recv(count)
        #         if not tmp_buf:
        #             return None
        #         buf += tmp_buf
        #         count -= len(tmp_buf)
        # except Exception:
        #     self.close_conn()
        # return buf


    def recv_all(self,count=0):
        buf = []
        try:
            # buf = self.img_socket.recv()
            get_size=1024*5
            while count:
                if get_size>count:
                    get_size=count
                tmp_buf = self.conn.recv(get_size)
                buf += tmp_buf
                # print(str(buf))
                count -= get_size
        except Exception as e:
            traceback.print_exc()
            # print(e)
            self.close_conn()
        # print('aaa')
        # print(buf)
        # print('bbb')
        return buf


    def recv_image(self):
        iReturn=None
        length = self.recv_size()
        # print(int(length))
        # print(str(length,'utf-8'))
        if length:
            stringData = self.recv_all(int(length))
            data = numpy.fromiter(stringData, dtype='uint8')
            iReturn = cv2.imdecode(data,1)
        return iReturn

    def send_response(self, msg):
        response_msg=bytes(msg,'utf-8')
        head_len_bytes = struct.pack('i', len(response_msg))
        self.conn.send(head_len_bytes)
        self.conn.sendall(response_msg)


    def send_image(self, image_data):
        stringData = image_data.tostring()
        # print(stringData)
        try:
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack('128sl',bytes('filename','utf-8'), len(stringData))
            self.img_socket.send(fhead)

            self.img_socket.sendall(stringData)
            # print(str(len(stringData)).ljust(16))
            # self.img_socket.send(bytes(str(len(stringData)).ljust(16),'utf-8'))
            # self.img_socket.send(stringData)
            # for i in range(0, len(stringData)):
            #     self.img_socket.send(bytes(str(stringData[i]),'utf-8'))

        except Exception as e:
            traceback.print_exc()
            self.close_conn()
