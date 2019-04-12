#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 29, 2018
XingTong
'''
import sys
from logger.StreamLogger import StreamLogger


class StreamBox(StreamLogger):
    '''
    the box which is used to package data in the pipeline
    '''
    def __init__(self):
        super(StreamBox,self).__init__()