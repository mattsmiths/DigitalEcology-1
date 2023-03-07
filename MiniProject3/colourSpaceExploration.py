#import modules
import numpy as np
import cv2

#Take in video live from webcam
cap = cv2.VideoCapture(0)
#check that camera can be used
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True: #Keep running forever
    #Read in a frame
    ret, frame = cap.read()
    #If frame is not read properly, stop
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    #Convert original frame into HSV colour space from BGR
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Define range of green color in HSV
    lower_green = np.array([40,10,10])
    upper_green = np.array([90,255,255])

    #Threshold the HSV image to get only green
    mask = cv2.inRange(hsv, lower_green, upper_green)

    #Make everything that is not green black(0)
    green = cv2.bitwise_and(frame,frame,mask=mask)

    #Make grayscale frame with BGR dimensions (3 layers instead of 1)
    gray = cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

    #Make everything that was green in the original frame black
    notgreen = cv2.bitwise_and(gray,gray,mask=cv2.bitwise_not(mask))


    #Display intermediate frames
    cv2.imshow('input', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('green', green)
    cv2.imshow('notgreen', notgreen)

    #Display green things as they are and everything else in grayscale
    cv2.imshow('output', notgreen+green)

    #Stop if any key is pressed
    keyCode = cv2.waitKey(10)
    print(keyCode)
    if keyCode != 255:
        break

#When everything is done, release the webcam
cap.release()
cv2.destroyAllWindows()