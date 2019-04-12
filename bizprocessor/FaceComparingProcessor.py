#!/usr/bin/env python
#coding: utf-8
'''
Created on Apr 09, 2019

@author: xingtong
'''
from baseprocessor.BaseProcessor import BaseProcessor
import os
import face_recognition

# def getWebPageSipder(appConfig):
#     mainPageUrl=appConfig.get('WebPageSpider','MAIN_PAGE_URL')
#     cookiePath=appConfig.get('WebPageSpider','COOKIE_PATH')
#     tempDocPath=appConfig.get('WebPageSpider','TEMP_DOC_PATH')
#     return WebPageSpider(mainPageUrl,cookiePath,tempDocPath)

class FaceComparingProcessor(BaseProcessor):
    '''
    this class is used to compare face code and get the target person
    '''

    def __init__(self,inputQueue=None,outputQueue=None):
        super(FaceComparingProcessor,self).__init__(inputQueue=inputQueue,outputQueue=outputQueue)
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_files = []
        self.get_all_images()

    def get_all_images(self):
        print('Begin load face image information')
        upper_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
        folder_path = os.path.join(upper_dir, 'images')
        # print(folder_path)
        files = os.listdir(folder_path)
        this_time_load_num = 0
        for file in files:
            if file not in self.load_files:
                this_time_load_num += 1
                image_path = os.path.join(folder_path, file)
                name = file.split('.')[0]
                face_image = face_recognition.load_image_file(image_path)
                face_image_coding = face_recognition.face_encodings(face_image)[0]
                self.known_face_encodings.append(face_image_coding)
                self.known_face_names.append(name)
                self.load_files.append(file)
        print("load face image information has finished. there are %d image"
              "being loaded at this time. there are %d image totally" % (this_time_load_num, len(self.load_files)))


    def process(self,processObj=None):
        if processObj is not None:

            face_encodings=processObj.face_encodings

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.3)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                else:
                    pass
                    # get a image name iname
                    # save the frame as image which is named after iname
                face_names.append(name)
            processObj.face_names=face_names
        return processObj

