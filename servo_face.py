#! /usr/bin/python

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle

import time
import cv2

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import RPi.GPIO as GPIO # 라즈베리파이 GPIO 핀을 쓰기위해 임포트
import time # 시간 간격으로 제어하기 위해 임포트

cred = credentials.Certificate('pill-dispenser-d4bec-firebase-adminsdk-116fy-ae1afad8ff.json')
firebase_admin.initialize_app(cred,{
	'databaseURL' : 'https://pill-dispenser-d4bec-default-rtdb.firebaseio.com'
})

def facial_recog():
    # Initialize 'currentname' to trigger only when a new person is identified.
    currentname = "unknown"
    # Determine faces from encodings.pickle file model created from train_model.py
    encodingsP = "encodings_cnn.pickle"
    # use this xml file
    cascade = "haarcascade_frontalface_default.xml"

    # load the known faces and embeddings along with OpenCV's Haar
    # cascade for face detection
    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open(encodingsP, "rb").read())
    detector = cv2.CascadeClassifier(cascade)

    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    # vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)

    # start the FPS counter
    fps = FPS().start()

    # loop over frames from the video file stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = vs.read()
        frame = imutils.resize(frame, width=500)

        # convert the input frame from (1) BGR to grayscale (for face
        # detection) and (2) from BGR to RGB (for face recognition)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # detect faces in the grayscale frame
        rects = detector.detectMultiScale(gray, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

        # OpenCV returns bounding box coordinates in (x, y, w, h) order
        # but we need them in (top, right, bottom, left) order, so we
        # need to do a bit of reordering
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
                                                     encoding)
            name = "Unknown"  # if face is not recognized, then print Unknown

            # check to see if we have found a match
            if True in matches:

                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

                # If someone in your dataset is identified, print their name on the screen
                if currentname != name:
                    currentname = name
                    print(currentname)

            # update the list of names
            names.append(name)

          #  firebase_data(currentname)


        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image - color is in BGR
            cv2.rectangle(frame, (left, top), (right, bottom),
                          (0, 255, 225), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        .8, (0, 255, 255), 2)

        # display the image to our screen
        cv2.imshow("Facial Recognition is Running", frame)
        key = cv2.waitKey(1) & 0xFF



        # quit when 'q' key is pressed
        if key == ord("q"):
            break

        # update the FPS counter
        fps.update()

        return currentname

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()




def firebase_data(name):
    currentname = name



    dir = db.reference('users/' + currentname + '/pill')
    pill_name = dir.get()
        # print(pill_name)
    first = pill_name.split('[')
    second = first[1]
        # print(second)
    third = second.split(']')
        # print(third[0])

    real_pill_name = third[0]

    dir_pill_day = db.reference('pill/' + currentname + '/' + real_pill_name + '/day')
    pill_day = dir_pill_day.get()
    #	print(pill_day)
    split_day = pill_day.split(',')
    # print(split_day[0])

    dir_pill_daytime = db.reference('pill/' + currentname + '/' + real_pill_name + '/daytime')
    pill_daytime = dir_pill_daytime.get()
    #	print(pill_daytime)
    split_daytime = pill_daytime.split(',')
    # print(split_daytime[0])

    dir_pill_time = db.reference('pill/' + currentname + '/' + real_pill_name + '/time')
    pill_time = dir_pill_time.get()
    #	print(pill_time)
    split_time = pill_time.split(',')
    # print(split_time[0])

    # list 만들어서 있는지 확인
    # 여러개 있는거
    # 먼저는 모터 하나만햇을떄 돌아가는 지확인

    print(change_name_day(split_day[0]))
    print(return_time(split_daytime[0], split_time[0]))

    return change_name_day(split_day[0]), return_time(split_daytime[0], split_time[0])


def change_name_day(day):
    if (day == '월'):
        eng_day = "Mon"
    elif (day == '화'):
        eng_day = "Tue"
    elif (day == '수'):
        eng_day = "Wed"
    elif (day == '목'):
        eng_day = "Thu"
    elif (day == '금'):
        eng_day = "Fri"
    elif (day == '토'):
        eng_day = "Sat"
    elif (day == '일'):
        eng_day = "Sun"

    return eng_day

def return_time(daytime, time):
    if (daytime == '아침'):
        if (time == '식전'):
            motor_time = "07:30:00"
        elif (time == '식후'):
            motor_time = "08:30:00"
    elif (daytime == '점심'):
        if (time == '식전'):
            motor_time = "12:00:00"
        elif (time == '식후'):
            motor_time = "12:30:00"
    elif (daytime == '저녁'):
        if (time == '식전'):
            motor_time = "18:00:00"
        elif (time == '식후'):
            motor_time = "19:30:00"

    return motor_time




def main():
    while(True):
        pi_name = facial_recog()
        pi_day, pi_time = firebase_data(pi_name)

   #facial_recog()

  #  print('name:',pi_name)
  #  print('day',pi_day)
 #   print('time',pi_time)

         GPIO.setmode(GPIO.BCM)
         SERVO = 13
         GPIO.setup(SERVO, GPIO.OUT)
         SERVO_PWM = GPIO.PWM(SERVO, 50)
         SERVO_PWM.start(0)

   # alarm_S = "08:00:00"
        #while (True):
        i = 1
        cur_time = time.ctime()
            # 요일, 월, 일, 시간, 년도 받아온다.
        ddmmss = cur_time.split(' ')[-2]
        #ddmmss = "19:30:00"

        if ddmmss == pi_time:
            while (i < 2):

            SERVO_PWM.ChangeDutyCycle(10)
            time.sleep(1)
            SERVO_PWM.ChangeDutyCycle(5)
            time.sleep(1)
            i = i + 1
            SERVO_PWM.stop()
            GPIO.cleanup()

if __name__ == '__main__':
    main()



