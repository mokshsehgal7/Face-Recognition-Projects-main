
# camera.py
# import the necessary packages
import cv2
# import cv2
import numpy as np
import face_recognition
import os
# defining face detector
# face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
# ds_factor = 0.6
path = 'Training_images'
images = []
classNames = ['Unknown']
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodeList = []


    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete')


class VideoCamera(object):
    def __init__(self):
        # capturing video
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        # releasing camera
        self.video.release()


    def get_frame(self):
        # extracting frames
        success, img = self.video.read()

        # success, img = cap.read()
        # cv2.imshow('ms',img)
        img1 = img
        # img = captureScreen()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex=0
            # print(faceDis[np.argmin(faceDis)])
            if faceDis[np.argmin(faceDis)]<=0.56:

                matchIndex = int(np.argmin(faceDis)+1)
                # print(matchIndex)
            # else:
            #     matchIndex=0

            # if matches[matchIndex]:
            #     print(matchIndex)
            name = classNames[int(matchIndex)].upper()
            print(name)
            # markAttendance(name)
            # cv2.imshow('Face Recognition', img)
            # cv2.waitKey(1)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 5), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)


        # cv2.imshow('cam', img)
        # if cv2.waitKey(1) == 13:
        #     break

    # cap.release()
    # cv2.destroyAllWindows()

        #
        # frame = cv2.resize(image, None, fx=ds_factor, fy=ds_factor,
        #                    interpolation=cv2.INTER_AREA)
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        # for (x, y, w, h) in face_rects:
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #     break
        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
