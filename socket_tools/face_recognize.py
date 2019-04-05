import face_recognition
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
        # Load a sample picture and learn how to recognize it.
        obama_image = face_recognition.load_image_file("xingtong1.jpg")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

        # Load a second sample picture and learn how to recognize it.
        biden_image = face_recognition.load_image_file("meinv.jpg")
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

        # Create arrays of known face encodings and their names
        self.known_face_encodings = [
            obama_face_encoding,
            biden_face_encoding
        ]
        self.known_face_names = [
            "XingTong",
            "Mei Nv"
        ]

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []

    def face_recognize(self, face_image=None,**kwargs):
        if face_image is None or len(face_image)==0:
            return

        # Resize frame of video to 1/2 size for faster face recognition processing
        # small_frame = cv2.resize(face_image, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        # rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(face_image)
        face_encodings = face_recognition.face_encodings(face_image, face_locations)

        # face_locations=kwargs.get('face_locations')
        # face_encodings=kwargs.get('face_encodings')

        face_names = []
        for face_encoding in face_encodings:
                # print(face_encoding)
                # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
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

        # process_this_frame = not process_this_frame

        # font = cv2.FONT_HERSHEY_DUPLEX
        # Display the results

        # for (top, right, bottom, left), name in zip(face_locations, face_names):
        #     # Scale back up face locations since the frame we detected in was scaled to 1/5 size
        #     top *= 4
        #     right *= 4
        #     bottom *= 4
        #     left *= 4
        #
        #     # Draw a box around the face
        #     cv2.rectangle(face_image, (left, top), (right, bottom), (0, 0, 255), 2)
        #
        #     # Draw a label with a name below the face
        #     cv2.rectangle(face_image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        #
        #     cv2.putText(face_image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        # return face_image
        return face_locations, face_names