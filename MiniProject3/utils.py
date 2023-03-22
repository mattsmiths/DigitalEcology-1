from tflite_runtime.interpreter import Interpreter 
from PIL import Image
import numpy as np
import time
import datetime
import cv2 as cv
import os
import csv

def load_labels(path): # Read the labels from the text file as a Python list.
	with open(path, 'r') as f:
		return [line.strip() for i, line in enumerate(f.readlines())]



def visualize(im1,bbx,clss,clsKey,scores,sz1,thresh=0.25):

    for ind1,detection in enumerate(bbx):
    # Draw bounding_box
        if scores[ind1] < thresh:
            continue
        #start_point = (int(detection[0]*sz1[1]),int(detection[1]*sz1[0]))
        #end_point = (detection[0]+detection[2])*sz1[1], (detection[1]+detection[3])*sz1[0]
        #end_point = int((detection[2])*sz1[1]), int((detection[3])*sz1[0])
        
        start_point = (int(detection[1]*sz1[1]),int(detection[0]*sz1[0]))
        end_point = int((detection[3])*sz1[1]),int((detection[2])*sz1[0])
        c1 = (55,240,50)
        thickness = 2
        cv.rectangle(im1, start_point, end_point,c1,thickness)

        # Draw label and score
        category_name = clsKey[int(clss[ind1])]
        probability = round(scores[ind1]*100, 2)
        result_text = category_name + ' (' + str(probability) + '%)'
        text_location = (start_point[0],start_point[1])
        cv.putText(im1, result_text, text_location, cv.FONT_HERSHEY_PLAIN,
                    3, (255,255,255), 4)
    return im1


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


#Create folder for saving detections in CSVs:
def detectionsFolderCreate():
	baseSave = '/home/pi/Documents/detections/'
	if not os.path.isdir('/home/pi/Documents/detections/'):
		os.mkdir('/home/pi/Documents/detections/')

	timeObj = datetime.datetime.now()
	tempDateName = '%s-%02d-%02d/'%(timeObj.year,timeObj.month,timeObj.day)
	if not os.path.isdir('/home/pi/Documents/detections/'+tempDateName):
		os.mkdir('/home/pi/Documents/detections/'+tempDateName)
		os.mkdir('/home/pi/Documents/detections/'+tempDateName+'images/')
	return tempDateName

def cmdline_run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--capture_stills', default=False, action='store_true',
        help='save single images when triggered')
    parser.add_argument(
        '-D', '--in_systemd', action='store_true',
        help='running in sysd, reset watchdog')
    parser.add_argument(
        '-f', '--fake', default=False, action='store_true',
        help='fake client detection')
    parser.add_argument(
        '-l', '--loc', type=str, required=True,
        help='camera locator (ip address or /dev/videoX)')
    parser.add_argument(
        '-n', '--name', default=None,
        help='camera name (overrides automatic name detection)')
    parser.add_argument(
        '-p', '--password', default=None,
        help='camera password')
    parser.add_argument(
        '-P', '--profile', default=False, action='store_true',
        help='profile (requires yappi)')
    parser.add_argument(
        '-r', '--retry', default=False, action='store_true',
        help='retry on acquisition errors')
    parser.add_argument(
        '-t', '--thumbnails', default=False, action='store_true',
        help='save downsampled images as thumbnails')
    parser.add_argument(
        '-u', '--user', default=None,
        help='camera username')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='enable verbose output')
    args = parser.parse_args()
