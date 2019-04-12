import face_recognition
import os
import cv2
import time
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)



class face_recognize(object):

    def __init__(self):

        # Create arrays of known face encodings and their names
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_files=[]

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.get_all_images()

    def get_all_images(self):
        print('Begin load face image information')
        upper_dir=os.path.abspath(os.path.join(os.getcwd(), ".."))
        folder_path = os.path.join(upper_dir,'images')
        # print(folder_path)
        files=os.listdir(folder_path)
        this_time_load_num=0
        for file in files:
            if file not in self.load_files:
                this_time_load_num+=1
                image_path = os.path.join(folder_path, file)
                name=file.split('.')[0]
                face_image=face_recognition.load_image_file(image_path)
                face_image_coding=face_recognition.face_encodings(face_image, num_jitters=3)[0]
                self.known_face_encodings.append(face_image_coding)
                self.known_face_names.append(name)
                self.load_files.append(file)
        print("load face image information has finished. there are %d image"
              "being loaded at this time. there are %d image totally" % (this_time_load_num, len(self.load_files)))


    def face_recognize(self, face_image=None,**kwargs):
        if face_image is None or len(face_image)==0:
            return
        (captured_location, captured_time, face_image) = face_image
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(face_image, number_of_times_to_upsample=2, model="hog")
        face_encodings=[]
        if len(face_locations)>0:
            face_encodings = face_recognition.face_encodings(face_image, face_locations, num_jitters=3)

        face_names = []
        for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.4)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]
            else:
                pass
                    #get a image name iname
                    #save the frame as image which is named after iname
            face_names.append(name)

        return captured_location, captured_time, face_locations, face_names