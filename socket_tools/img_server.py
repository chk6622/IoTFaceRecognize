#!/usr/bin/python
#-*-coding:utf-8 -*-

from socket_tools.img_socket_tool_pro import img_socket_tool
from socket_tools.face_recognize import face_recognize
import cv2
import numpy
import time


if __name__=='__main__':



    this_port = 8080
    this_ip = 'localhost'
    server = img_socket_tool(this_ip, this_port)
    server.create_server()

    # time.sleep(5)
    #
    # remote_port = 8081
    # remote_ip = 'localhost'
    # client = img_socket_tool(remote_ip, remote_port)
    # client.connect_server()




    fr=face_recognize()
    font = cv2.FONT_HERSHEY_DUPLEX
    while True:
        # time.sleep(0.05)
        frame_info=server.recv_data()
        if frame_info is None:
            continue
        face_locations, face_names=fr.face_recognize(face_image=frame_info)
        response_msg={}
        response_msg['face_locations']=face_locations
        response_msg['face_names']=face_names
        server.send_data(response_msg)
        # print(face_locations, face_names)
        # if image is not None:
        #     cv2.putText(image, '123', (5, 30), font, 1.0, (255, 255, 255), 1)
        #     cv2.namedWindow("Image")
        #     cv2.imshow("Image", image)
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break

    server.close_conn()
    client.close_conn()
    # cv2.destroyAllWindows()