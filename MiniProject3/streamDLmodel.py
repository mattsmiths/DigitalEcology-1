"""
Script that will load the specified model [ classification or detection ]
- opens stream to display results
- takes arguments in the form of flags through command line
- "--resolution" inputs are "small", "medium", "medium2","large"
- "--detection" will call a detection model, else classification model
- "--threshold" sets the threshold for inclusion of inferred data
- "--birds" set true for loading the specified model trained on only birds from iNaturalist dataset
- "--no_saved_stills" turns off saving still images 
"""


#import modules
from tflite_runtime.interpreter import Interpreter 
from PIL import Image
import numpy as np
import time
import datetime
import cv2 as cv
import os
import csv
import utils
font = cv.FONT_HERSHEY_DUPLEX




args = utils.cmdline_run()
detectModel = args.detection
onlyBirds = args.birds
inclusionThreshold = float(args.threshold)
no_saved_stills = args.no_saved_stills
if float(inclusionThreshold) > 1:inclusionThreshold/=100



#### Loading in models based on command line arguments ####

# Setting directory paths for models and corresponding labels
data_folder = "/home/pi/DigitalEcologyDL/MiniProject3/models/"
if not detectModel:
    if not onlyBirds:
        model_path = data_folder + "lite-model_imagenet_mobilenet_v3_large_075_224_classification_5_metadata_1.tflite"
        labels = utils.load_labels("/home/pi/DigitalEcologyDL/MiniProject3/labels/imageNetLabels.txt")
    else:
        model_path = data_folder + "mobileV2_fullTrain_aves_model.tflite"
        labels = utils.load_labels("/home/pi/DigitalEcologyDL/MiniProject3/labels/mobileV2_aves_labels.txt")

elif detectModel == True:
    if not onlyBirds:
        model_path = data_folder + "lite-model_efficientdet_lite1_detection_metadata_1.tflite"
        labels = utils.load_labels("/home/pi/DigitalEcologyDL/MiniProject3/labels/coco-labels-paper.txt")
    else:
        print('Detection model trained on birds is currently training (~6 hours left)')
        print('Loading efficientDet trained on COCO dataset temporarily')
        model_path = data_folder + "lite-model_efficientdet_lite1_detection_metadata_1.tflite"
        labels = utils.load_labels("/home/pi/DigitalEcologyDL/MiniProject3/labels/coco-labels-paper.txt")
    
    
interpreter = Interpreter(model_path)
print("Model Loaded Successfully.")
interpreter.allocate_tensors()
_, height, width, _ = interpreter.get_input_details()[0]['shape']
print("Image Shape (", width, ",", height, ")")


input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_index = interpreter.get_input_details()[0]["index"]
output_index = interpreter.get_output_details()[0]["index"]
if detectModel:
    output_indexC  = interpreter.get_output_details()[1]["index"]
    output_indexS = interpreter.get_output_details()[2]["index"]


#Set the image resolution as specified by command line arguments
imageResolution = utils.resolutionKey(args.resolution)
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



# Create the directory to save detections
tempDateName = utils.detectionsFolderCreate()



#check that camera can be used
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# confirm the image size
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
    
    image = cv.resize(frame[:,:,::-1],(width,height))
    #image = cv.resize(frame,(width,height))
    #image = (np.expand_dims(image,0)).astype(np.float32)
    
    if detectModel:
        image = (np.expand_dims(image,0)).astype(np.uint8)
    else:
        image = (np.expand_dims(image/255,0)).astype(np.float32)
    
    #Run inference from model
    interpreter.set_tensor(input_index, image)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_index)
    
    
    #FPS estimate
    fpsTail.append(time.time()-ts1)
    if len(fpsTail)>5:fpsTail.pop(0)
    fpsFinal = np.nanmean(fpsTail)
    
    #Post-processing for classification models
    if not detectModel:
        # Return the classification label of the image.
        label_id = np.argmax(predictions)
        classification_label = '[ %s ]'%labels[label_id]
        confidence = utils.softmax(predictions)[0]
        mConf = np.round(confidence[np.argmax(confidence)]*100,2)
        iConf = confidence[np.argmax(confidence)]
        ind = np.argsort(confidence)[-3:]
        ccs = [np.round(elem*100,2) for elem in confidence[ind]]
        lbl2 = '[ %s ]'%labels[ind[-2]]
        lbl3 = '[ %s ]'%labels[ind[-3]]
        
        #Display frame
        cv.putText(frame,'1 - '+classification_label+': %s'%mConf+'% confidence',(int(imWidth*0.15),int(imHeight*0.14)),font,fontScale=(0.5*(imageResolution[0]/640)),color=(125,55,235),thickness=1)
        cv.putText(frame,'2 - '+lbl2+': %s'%ccs[-2]+'% confidence',(int(imWidth*0.15),int(imHeight*0.18)),font,fontScale=(0.5*(imageResolution[0]/640)),color=(125,55,235),thickness=1)
        cv.putText(frame,'3 - '+lbl3+': %s'%ccs[-3]+'% confidence',(int(imWidth*0.15),int(imHeight*0.22)),font,fontScale=(0.5*(imageResolution[0]/640)),color=(125,55,235),thickness=1)
        cv.putText(frame,'fps: %s '%np.round(1/fpsFinal,3),(int(imWidth*0.15),int(imHeight*0.08)),font,fontScale=(0.5*(imageResolution[0]/640)),color=(125,55,235),thickness=1)
        cv.imshow('output', frame)
        
        if iConf > inclusionThreshold:
            tname = datetime.datetime.now()
            imName = '%s-%02d-%02d_%02d-%02d-%02d'%(tname.year,tname.month,tname.day,tname.hour,tname.minute,tname.second)
            imName_s = '%s-%02d-%02d_%02d'%(tname.year,tname.month,tname.day,tname.hour)
            imNameSave = '/home/pi/Documents/detections/'+tempDateName+'images/'+imName+'.jpg'
            if not no_saved_stills:
                cv.imwrite(imNameSave,frame)
            
            detctSave = '/home/pi/Documents/detections/'+tempDateName+imName_s+'.csv'
            if os.path.isfile(detctSave) == False: #make new file everyday??
                f = open(detctSave, 'w')
                writer = csv.writer(f)
                heads = ['date','image','class','confidence']
                writer.writerow(heads)
                f.close()
                
            
            finalLine = [imName,imNameSave,classification_label,mConf]
            f = open(detctSave, 'a')
            writer = csv.writer(f)
            writer.writerow(finalLine)
            f.close()
            
            
    else:
        labelsDetect = interpreter.get_tensor(output_indexC)
        scre = interpreter.get_tensor(output_indexS)
        frame = utils.visualize(frame,predictions[0],labelsDetect[0],labels,scre[0],(imHeight,imWidth),0.23)
        cv.imshow('output', frame)
        
        mConf = scre[0][0]
        classification_label = labels[int(labelsDetect[0][0])]
        if mConf > inclusionThreshold:
            
            tname = datetime.datetime.now()
            imName = '%s-%02d-%02d_%02d-%02d-%02d'%(tname.year,tname.month,tname.day,tname.hour,tname.minute,tname.second)
            imName_s = '%s-%02d-%02d_%02d'%(tname.year,tname.month,tname.day,tname.hour)
            imNameSave = '/home/pi/Documents/detections/'+tempDateName+'images/'+imName+'.jpg'
            if not no_saved_stills:
                cv.imwrite(imNameSave,frame)
            
            detctSave = '/home/pi/Documents/detections/'+tempDateName+imName_s+'.csv'
            if os.path.isfile(detctSave) == False: #make new file every??
                f = open(detctSave, 'w')
                writer = csv.writer(f)
                heads = ['date','image','class','confidence']
                writer.writerow(heads)
                f.close()
                
            
            finalLine = [imName,imNameSave,classification_label,mConf]
            f = open(detctSave, 'a')
            writer = csv.writer(f)
            writer.writerow(finalLine)
            f.close()
    
    # Stop if any key is pressed
    keyCode = cv.waitKey(10)
    print(keyCode)
    if keyCode != 255:
        break
    if camSave >0:camSave-=1
    
    
#When everything is done, release the webcam
cap.release()
cv.destroyAllWindows()


