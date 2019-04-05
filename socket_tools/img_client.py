#!/usr/bin/python
#-*-coding:utf-8 -*-

from socket_tools.connection_tool import connector
import cv2
import numpy
import time
import face_recognition

def recognize_face(frame,resize=0.5):
    small_frame = cv2.resize(frame, (0, 0), fx=resize, fy=resize)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    client.send_data(rgb_small_frame)
    response_msg = client.recv_data()
    return response_msg

if __name__=='__main__':
    remote_port=8080
    remote_ip='localhost'
    client=connector(remote_ip, remote_port)
    client.create_client()

    resize=0.5 # Resize frame of video  for faster face recognition processing
    recoverParam=int(1/resize)
    skip_frames=5
    capture = cv2.VideoCapture(0)
    # ret, frame = capture.read()

    font = cv2.FONT_HERSHEY_DUPLEX

    response_msg = None
    index=1
    while True:
        index+=1
        if index>=10000000:
            index=1
        ret, frame = capture.read()
        if not ret:
            break

        if index%skip_frames==0:
            response_msg=recognize_face(frame)

            # small_frame = cv2.resize(frame, (0, 0), fx=resize, fy=resize)
            #
            # # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            # rgb_small_frame = small_frame[:, :, ::-1]
            #
            # client.send_data(rgb_small_frame)
            # response_msg = client.recv_data()
        else:
            time.sleep(0.02)

        if response_msg is not None:
            face_locations = response_msg.get('face_locations')
            face_names = response_msg.get('face_names')
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= recoverParam
                right *= recoverParam
                bottom *= recoverParam
                left *= recoverParam

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.namedWindow("Image")
        cv2.imshow("Image", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



    client.close_conn()
    cv2.destroyAllWindows()