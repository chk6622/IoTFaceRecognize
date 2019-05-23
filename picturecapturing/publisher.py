# import paho.mqtt.publish as mqtt
import paho.mqtt.client as mqtt
import ssl
import cv2
import numpy as np
import time


def get_video_info(cap):
    '''
    get the video information
    @return: video information
    '''
    video_info = {
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'num_of_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT))}
    return video_info


if __name__ == '__main__':
    HOST = "a2xskqc7e823wb-ats.iot.ap-southeast-2.amazonaws.com"
    PORT = 8883
    university='AUT'
    classroom='WZ313' 
    client = mqtt.Client()
    caPath = "./AmazonRootCA1.pem" # Root certificate authority, comes from AWS with a long, long name
    certPath = "./8aab8da6e0-certificate.pem.crt"
    keyPath = "./8aab8da6e0-private.pem.key"

    client.tls_set(caPath, 
        certfile=certPath, 
        keyfile=keyPath, 
        cert_reqs=ssl.CERT_REQUIRED, 
        tls_version=ssl.PROTOCOL_TLSv1_2, 
        ciphers=None)
    
    

    cap=cv2.VideoCapture(0)

    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    print(get_video_info(cap))
    while True:
        ret, frame = cap.read()
        if frame is None:
            continue
        topic = '%s/%s/%s' % (university,classroom,time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
        result,encimg = cv2.imencode('.jpg', frame, encode_param)
        data_encode = np.array(encimg)  
        str_encode = data_encode.tostring()
        
        client.connect(HOST, PORT)
        result,index = client.publish(topic, str_encode, qos = 0)
        client.disconnect()
        
        if result==4:
            err='MQTT_ERR_NO_CONN'
            print(err)
        else:
            print(result,index)
        
        time.sleep(0.2)