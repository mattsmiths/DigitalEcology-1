#import modules

from tflite_runtime.interpreter import Interpreter 
from PIL import Image
import numpy as np
import time
import datetime
import cv2 as cv
font = cv.FONT_HERSHEY_DUPLEX


#imageResolution = (2592,1944)
#imageResolution = (1920,1080)
#imageResolution = (1280,720)
imageResolution = (640,480)
#focus = 128# min= 128 (focal distance farther) , max = 990 (focal distance is closer)

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.nanmax(x))
    return e_x / np.nansum(e_x)

def classify_image(interpreter, image, top_k=1):
  tensor_index = interpreter.get_input_details()[0]['index']
  interpreter.set_tensor(tensor_index, image)

  interpreter.invoke()
  output_details = interpreter.get_output_details()[0]
  output = np.squeeze(interpreter.get_tensor(output_details['index']))

  scale, zero_point = output_details['quantization']
  output = scale * (output - zero_point)

  ordered = np.argpartition(-output, top_k)
  return [(i, output[i]) for i in ordered[:top_k]][0]


def load_labels(path): # Read the labels from the text file as a Python list.
  with open(path, 'r') as f:
    return [line.strip() for i, line in enumerate(f.readlines())]

data_folder = "/home/pi/Downloads/"
model_path = data_folder + "lite-model_imagenet_mobilenet_v3_large_075_224_classification_5_metadata_1.tflite"
#label_path = data_folder + "labels_mobilenet_quant_v1_224.txt"
interpreter = Interpreter(model_path)
print("Model Loaded Successfully.")
interpreter.allocate_tensors()
_, height, width, _ = interpreter.get_input_details()[0]['shape']
print("Image Shape (", width, ",", height, ")")

# Read class labels.
labels = load_labels("/home/pi/Downloads/labels.txt")

#interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_index = interpreter.get_input_details()[0]["index"]
output_index = interpreter.get_output_details()[0]["index"]



#Take in video live from webcam
cap = cv.VideoCapture('/dev/video0')
attr = getattr(cv,'CAP_PROP_FRAME_WIDTH')
cap.set(attr,imageResolution[0])
attr = getattr(cv,'CAP_PROP_FRAME_HEIGHT')
cap.set(attr,imageResolution[1])
attr = getattr(cv,'CAP_PROP_AUTOFOCUS')
cap.set(attr,1)
attr = getattr(cv,'CAP_PROP_FPS')
cap.set(attr,30)
#attr = cap.getattr(cv,'CAP_PROP_FOCUS')
#cap.set(attr,focus)



#check that camera can be used
if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
ret,frame = cap.read()
imHeight,imWidth,imZ = np.shape(frame)

fpsTail = []
camSave = 0

while True: #Keep running forever
    #Read in a frame
    ts1 = time.time()
    ret, frame = cap.read()
    
    #If frame is not read properly, stop
    if not ret:
        if camSave < 5:
            print("Can't receive frame (stream end?). Restarting ... attempt #%s"%camSave)
            cap.release()
            cap = cv.VideoCapture('/dev/video0')
            camSave+=1
            continue
        else:
            print('stopping stream')
            break
    
    image = cv.resize(frame,(width,height))
    #image = (np.expand_dims(image,0)).astype(np.float32)
    image = (np.expand_dims(image,0)/255).astype(np.float32)
    
    #Run inference from model
    interpreter.set_tensor(input_index, image)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_index)
    
    # Return the classification label of the image.
    label_id = np.argmax(predictions)
    classification_label = '[ %s ]'%labels[label_id]
    confidence = softmax(predictions)[0]
    mConf = np.round(confidence[np.argmax(confidence)]*100,2)
    ind = np.argsort(confidence)[-3:]
    ccs = [np.round(elem*100,2) for elem in confidence[ind]]
    lbl2 = '[ %s ]'%labels[ind[-2]]
    lbl3 = '[ %s ]'%labels[ind[-3]]
    
    #FPS estimate
    fpsTail.append(time.time()-ts1)
    if len(fpsTail)>5:fpsTail.pop(0)
    fpsFinal = np.nanmean(fpsTail)
    #Display frame
    cv.putText(frame,'1 - '+classification_label+': %s'%mConf+'% confidence',(int(imWidth*0.15),int(imHeight*0.14)),font,fontScale=(0.5*(imageResolution[0]/640)),color=(125,55,235),thickness=1)
    cv.putText(frame,'2 - '+lbl2+': %s'%ccs[-2]+'% confidence',(int(imWidth*0.15),int(imHeight*0.18)),font,fontScale=(0.5*(imageResolution[0]/640)),color=(125,55,235),thickness=1)
    cv.putText(frame,'3 - '+lbl3+': %s'%ccs[-3]+'% confidence',(int(imWidth*0.15),int(imHeight*0.22)),font,fontScale=(0.5*(imageResolution[0]/640)),color=(125,55,235),thickness=1)
    cv.putText(frame,'fps: %s '%np.round(1/fpsFinal,3),(int(imWidth*0.15),int(imHeight*0.08)),font,fontScale=(0.5*(imageResolution[0]/640)),color=(125,55,235),thickness=1)
    cv.imshow('output', frame)
    
    # Stop if any key is pressed
    keyCode = cv.waitKey(10)
    print(keyCode)
    if keyCode != -1:
        break
    if camSave >0:camSave-=1
#When everything is done, release the webcam
cap.release()
cv.destroyAllWindows()
