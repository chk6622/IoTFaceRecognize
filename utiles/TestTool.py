#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 21, 2018

@author: xingtong
'''


def fun1():
    while True:
        yield 1


fun2=fun1()
print(next(fun2))


