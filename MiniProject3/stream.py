#import modules
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

    #Display frame
    cv2.imshow('output', frame)

    # Stop if any key is pressed
    keyCode = cv2.waitKey(10)
    print(keyCode)
    if keyCode != 255:
        break

#When everything is done, release the webcam
cap.release()
cv2.destroyAllWindows()