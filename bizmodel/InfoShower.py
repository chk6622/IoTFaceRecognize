#!/usr/bin/python
#-*-coding:utf-8 -*-
'''
Created on Apr 8, 2019

@author: xingtong
'''

class InfoShower(object):
    def __init__(self):
        self.captured_info=[]
        # self.input_begin_index=0
        self.show_begin_index = 0
        self.show_end_index = 0
        self.show_size = 20

    def add_captured_info(self,captured_info):
        if captured_info is not None:
            self.captured_info.append(captured_info)
            self.captured_info = list(set(self.captured_info))  #remove repeat
            self.captured_info.sort(reverse=True)


    def get_show_info(self):
        lReturn=None
        list_length=len(self.captured_info)
        self.show_end_index += 1
        # end_index= self.show_begin_index + self.show_size
        if self.show_end_index > list_length:
            self.show_end_index = list_length
        if self.show_end_index - self.show_begin_index > self.show_size:
            self.show_begin_index += 1
        lReturn = self.captured_info[self.show_begin_index:self.show_end_index]
        return lReturn

if __name__=='__main__':
    ins = InfoShower()
    ins.add_captured_info(1)
    ins.add_captured_info(1)
    for i in range(1,10):
        ins.add_captured_info(i)
    for i in range(1,10):
        print(ins.get_show_info())
