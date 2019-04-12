#!/usr/bin/env python
#coding: utf-8
'''
Created on Apr 12, 2019
XingTong
'''

import mysql.connector

from peewee import *
#
db = MySQLDatabase("AttendenceRecord", host="192.168.43.129", port=3306, user="root", passwd="xhy121230")
db.connect()

class BaseModel(Model):

    class Meta:
        database = db


class attendence_form(BaseModel):
    student_name = CharField()
    location= CharField()
    datetime= CharField()



if __name__=='__main__':
    if not attendence_form.table_exists():
        attendence_form.create_table()
    form1=attendence_form.create(location='wz313',datetime='20190412143101',student_name='XingTong')