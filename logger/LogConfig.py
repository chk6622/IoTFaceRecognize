#!/usr/bin/env python
#coding: utf-8
'''
Created on Apr 09, 2019

@author: xingtong
'''

import os
import logging.config

BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.config.fileConfig(os.path.join(BASE_DIR,'logger','../logging.conf'))
appLogger = logging.getLogger("FaceRecognizing")