#!/usr/bin/env python
#coding: utf-8
'''
Created on Apr 20, 2019

@author: xingtong
'''

import paho.mqtt.client as mqtt
import time
import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
from random import uniform
import json
import base64
import logging
import sys
import cv2
import numpy as np

BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class MqttTool(object):
    def __init__(self):
        self.HOST = "a2xskqc7e823wb-ats.iot.ap-southeast-2.amazonaws.com"
        self.PORT = 8883
        self.topic = 'aut/#'
        self.caPath = os.path.join(BASE_DIR,'security','AmazonRootCA1.pem')  # Root certificate authority, comes from AWS with a long, long name
        self.certPath = os.path.join(BASE_DIR,'security','8aab8da6e0-certificate.pem.crt')
        self.keyPath = os.path.join(BASE_DIR,'security','8aab8da6e0-private.pem.key')
        print(self.caPath)
        client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        userData=1
        self.client = mqtt.Client(client_id,userdata=userData)
        self.client.tls_set(self.caPath,
                       certfile=self.certPath,
                       keyfile=self.keyPath,
                       cert_reqs=ssl.CERT_REQUIRED,
                       tls_version=ssl.PROTOCOL_TLSv1_2,
                       ciphers=None)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log
        self.client.connect(self.HOST, self.PORT)
        self.client.recv_topic = None
        self.client.recv_data = None

    def on_connect(self, client, userdata, flags, rc):
        print(userdata)
        print("Connected with result code " + str(rc))
        client.subscribe(self.topic, 0)

    def on_message(self, client, userdata, msg):
        print(userdata)
        client.recv_topic=msg.topic
        client.recv_data=msg.payload

    def on_log(self, client, userdata, level, buf):
        print(buf)

    def recvDataFromServer(self):
        self.client.loop()
        rTopic,rData = (self.client.recv_topic,self.client.recv_data)
        self.client.recv_topic=None
        self.client.recv_data=None
        return rTopic,rData

    def close(self):
        self.client.disconnect()

if __name__=='__main__':
    mt=MqttTool()
    while True:
        topic,data=mt.recvDataFromServer()
        time.sleep(1)
    print(topic)

