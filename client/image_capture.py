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


if __name__=='__main__':
    maxsize=10
    inputQueue=Queue()
    outputQueue=Queue()
    image_send=image_send(inputQueue,outputQueue)
    image_send.daemon=True
    image_send.start()

    # resize=0.25 # Resize frame of video  for faster face recognition processing
    # recoverParam=4#int(1/resize)
    skip_frames=10
    upper_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
    video_path = os.path.join(upper_dir, 'video','test_1.mp4')
    # print(video_path)
    capture = cv2.VideoCapture(video_path)



    font = cv2.FONT_HERSHEY_DUPLEX

    response_msg = None
    index=1
    names=set()
    display_names=[]
    the_last_name_index=0
    while True:
        index+=1
        if index>=10000000:
            index=1
        ret, frame = capture.read()
        if not ret:
            break

        if index%skip_frames==0:
            inputQueue.put(frame.copy())
            time.sleep(2)
        else:
            time.sleep(0.2)
            continue
        #
        if outputQueue.qsize()>0:
            response_msg=outputQueue.get(block=True)

        if response_msg is not None:
            for (top, right, bottom, left, name) in response_msg:
                # Draw a box around the face
                # print(top, right, bottom, left, name)
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                time1 = datetime.now()
                names.add(time1.strftime('%Y-%m-%d %H:%M:%S')+' : '+name)

                # Draw a label with a name below the face
                # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

                # cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        if index%30==0:
            # name_set=set(names)
            name_length=len(names)
            if the_last_name_index>(name_length-1):
                the_last_name_index=name_length-1
            name_list=list(names)
            for i in range(the_last_name_index):
                display_names.append(name_list[i])
            the_last_name_index+=1
        display_names.sort(reverse=True)
        for (ind,name) in enumerate(display_names):
            print(name)
            cv2.putText(frame, name, (100, 300-ind*15), font, 0.5, (255, 255, 255), 1)

        # big_frame = cv2.resize(frame, (0, 0), fx=1.5, fy=1.5)
        cv2.namedWindow("Image")
        cv2.imshow("Image", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()