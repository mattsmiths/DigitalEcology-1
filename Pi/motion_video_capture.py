# importing OpenCV, time and Pandas library
import time
# importing datetime class from datetime library
from datetime import datetime

import cv2
import pandas

# Assigning reference frame (initially empty)
ref_frame = None

# Initializing DataFrame, one column is start
# time and other column is end time
df = pandas.DataFrame(columns = ["Start", "End"])

# Capturing video
cap= cv2.VideoCapture(2)

width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))



def write_video(tm):
    filename = str(tm.year) + '-' + str(tm.month) + '-' + str(tm.day) + '_' + str(tm.hour) + '-' + str(tm.minute) + '-' + str(tm.second) + '.mp4'
    writer= cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))

    video_length = 10
    start_time = time.time()

    while(int(time.time() - start_time) < video_length):
        ret,frame= cap.read()

        writer.write(frame)

        cv2.imshow('frame', frame)

    writer.release()


# Infinite while loop to treat stack of image as video
while True:
	# Reading frame(image) from video
	check, frame = cap.read()

	# Initializing motion = 0(no motion)
	motion = 0

	# Converting color image to gray_scale image
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Converting gray scale image to GaussianBlur
	# so that change can be find easily
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# In first iteration we assign the first collected frame
    # to the reference frame
	if ref_frame is None:
		ref_frame = gray
		continue

	# Difference between static background
	# and current frame(which is GaussianBlur)
	diff_frame = cv2.absdiff(ref_frame, gray)

	# If change in between static background and
	# current frame is greater than 30 it will show white color(255)
	thresh_frame = cv2.threshold(diff_frame, 20, 255, cv2.THRESH_BINARY)[1]
	thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
	cv2.imshow("Threshold Frame", thresh_frame)

	# Finding contour of moving object
	cnts,_ = cv2.findContours(thresh_frame.copy(),
		cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for contour in cnts:
		if cv2.contourArea(contour) < 10000:
			continue
		motion = 1
            
    # Make current frame into previous frame
	ref_frame = gray
	
	if motion == 1:
		print('motion detected!')
		tm = datetime.now()
		write_video(tm)
		ref_frame = None #reset reference frame to none to re-initalize
    
# Destroying all the windows

print('test')
cap.release()
cv2.destroyAllWindows()
