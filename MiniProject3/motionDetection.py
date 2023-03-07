#import modules
import numpy as np
import cv2
import csv


#model for background subtraction
backSub = cv2.createBackgroundSubtractorMOG2()

#Take in video live from webcam
cap = cv2.VideoCapture(0)

#check that camera can be used
if not cap.isOpened():
    print('Cannot open camera')
    exit()

frameNum = 0
while True: #Keep running forever
    #Read in a frame
    ret, frame = cap.read()
    #If frame is not read properly, stop
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    #Create mask of moving objects
    fgMask =  cv2.threshold(backSub.apply(frame),130,255,cv2.THRESH_BINARY)[1]
    maskOut = cv2.cvtColor(fgMask, cv2.COLOR_GRAY2BGR)

    #Find regions of same colour
    contours = cv2.findContours(fgMask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[1]

    if contours is not None:
        #Select contours of appropriate size
        contours = [blob for blob in contours if 2000 < cv2.contourArea(blob) < 20000]

        #Only record white contours (moving objects)
        lefts = [tuple(c[c[:,:,0].argmin()][0]) for c in contours]
        leftcolours = [fgMask[l[1], l[0]+1] for l in lefts]
        white = [contours[i] for i in range(len(contours)) if (leftcolours[i] == 255)]
        for cnt in white:
            movement = cv2.moments(cnt)
            cx = int(movement['m10']/movement['m00'])
            cy = int(movement['m01']/movement['m00'])
            cv2.circle(maskOut,(cx,cy), 5, (255,255,0), -1)

    #Display frame in real time
    cv2.imshow('output', maskOut)

    # Stop if any key is pressed
    keyCode = cv2.waitKey(10)
    print(keyCode)
    if keyCode != 255:
        break

    frameNum = frameNum + 1

#When everything is done, release the webcam and output video file
cap.release()
cv2.destroyAllWindows()