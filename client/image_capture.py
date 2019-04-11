#!/usr/bin/python
#-*-coding:utf-8 -*-
from typing import Union

from socket_tools.connection_tool import connector
import cv2
import numpy
import time
import face_recognition
from multiprocessing import Queue
from client.image_send import image_send
from datetime import datetime
import os
import numpy as np
from bizmodel.InfoShower import InfoShower


if __name__=='__main__':
    maxsize=10
    inputQueue=Queue()
    outputQueue=Queue()
    image_send=image_send(inputQueue,outputQueue)
    image_send.daemon=True
    image_send.start()

    # resize=0.25 # Resize frame of video  for faster face recognition processing
    # recoverParam=4#int(1/resize)
    skip_frames = 30
    upper_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
    video_path = os.path.join(upper_dir, 'video','test_3.mp4')
    # print(video_path)
    capture = cv2.VideoCapture(0)



    font = cv2.FONT_HERSHEY_DUPLEX

    response_msg = None
    index=1
    names=set()
    display_names=[]
    the_last_name_index=0
    recogn_frame=None
    temp_recogn_frame=None
    info_shower=InfoShower()
    print_infos = []

    isSend = True
    while True:
        index+=1
        if index>=10000000:
            index=1
        ret, frame = capture.read()
        if not ret:
            break

        if frame is not None:
            height, width, col = frame.shape

        if isSend: #index%skip_frames==0:
            recogn_frame = frame.copy()
            inputQueue.put(recogn_frame)
            isSend = False
        else:
            time.sleep(0.05)

        # if recogn_frame is not None:
        #     temp_recogn_frame = recogn_frame.copy()

        if outputQueue.qsize() > 0:
            response_msg = outputQueue.get()
            isSend = True

        if response_msg is not None:
            temp_recogn_frame = recogn_frame.copy()
            for (captured_location, captured_time, top, right, bottom, left, name) in response_msg:
                cv2.rectangle(temp_recogn_frame, (left, top), (right, bottom), (0, 0, 255), 2)
                info_shower.add_captured_info('%s,%s,%s is detected' % (captured_location, captured_time, name))
            print_infos = info_shower.get_show_info()
            ind = 1
            for print_info in print_infos:
                cv2.putText(temp_recogn_frame, print_info, (10, height-10-ind*15), font, 0.5, (255, 255, 255), 1)
                ind += 2
            response_msg = None

        cv2.namedWindow("Image")
        if temp_recogn_frame is not None:
            cv2.imshow("Image", np.hstack([frame, temp_recogn_frame]))
        elif recogn_frame is not None:
            cv2.imshow("Image", np.hstack([frame, recogn_frame]))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()