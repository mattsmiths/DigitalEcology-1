import cv2, time

cap= cv2.VideoCapture(2)

width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

def write_video():
    filename = str(time.time())+'.mp4'
    writer= cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))

    video_length = 10
    start_time = time.time()

    while(int(time.time() - start_time) < video_length):
        ret,frame= cap.read()

        writer.write(frame)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break


    cap.release()
    writer.release()
    cv2.destroyAllWindows()

write_video()