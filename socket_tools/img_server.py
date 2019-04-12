#!/usr/bin/python
#-*-coding:utf-8 -*-

from socket_tools.connection_tool import connector
from socket_tools.face_recognize import face_recognize
import cv2,time
import numpy
import time


if __name__=='__main__':



    this_port = 8080
    this_ip = 'localhost'
    server = connector(this_ip, this_port)
    server.create_server()


    fr=face_recognize()
    font = cv2.FONT_HERSHEY_DUPLEX
    while True:
        # time.sleep(0.05)
        frame_info=server.recv_data()
        if frame_info is None:
            time.sleep(0.1)
            continue
        captured_location, captured_time, face_locations, face_names = fr.face_recognize(face_image=frame_info)
        response_msg = {}
        response_msg['captured_location'] = captured_location
        response_msg['captured_time'] = captured_time
        response_msg['face_locations'] = face_locations
        response_msg['face_names'] = face_names
        server.send_data(response_msg)

    server.close_conn()
    client.close_conn()