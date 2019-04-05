#!/usr/bin/python
#-*-coding:utf-8 -*-

from socket_tools.img_socket_tool_pro import img_socket_tool
import cv2
import numpy
import time
import face_recognition


if __name__=='__main__':
    remote_port=8080
    remote_ip='localhost'
    client=img_socket_tool(remote_ip,remote_port)
    client.create_client()

    # this_port=8081
    # this_ip='localhost'
    # server=img_socket_tool(this_ip,this_port)
    # server.create_server()


    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()

    font = cv2.FONT_HERSHEY_DUPLEX

    response_msg = None
    index=1
    while ret:
        index+=1
        if index>=10000000:
            index=1
        ret, frame = capture.read()




        if index%5==0:
            # Resize frame of video to 1/2 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

            # result, imgencode = cv2.imencode('.jpg', frame)
            # data = numpy.array(imgencode)
            # data = numpy.array(small_frame)
            # face_locations = face_recognition.face_locations(rgb_small_frame)
            # face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            # send_msg = {}
            # send_msg['face_locations'] = face_locations
            # send_msg['face_encodings'] = face_encodings
            client.send_data(rgb_small_frame)
            response_msg = client.recv_data()
        else:
            time.sleep(0.02)

        if response_msg is not None:
            face_locations = response_msg.get('face_locations')
            face_names = response_msg.get('face_names')
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/5 size
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

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
    server.close_conn()
    cv2.destroyAllWindows()