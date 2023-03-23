# Bird feeder activity

Scripts and tutorials for Entomology 375: Digital Ecology

University of Wisconsin-Madison, Spring 2023

Developed by: Matt Smith

Further instructions available at: https://docs.google.com/document/d/1_DRVoc30KfV1LgBovR911WRT9VqHDDBkiwnvH4ZhpVg/edit?usp=sharing

# Set up
```bash
wget https://tfhub.dev/google/lite-model/imagenet/mobilenet_v3_large_075_224/classification/5/default/1?lite-format=tflite
sudo apt install libatlas-base-dev
pip3 install --no-deps  https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
```

Install libraries
```bash
sudo apt-get install libedgetpu1-std
sudo apt install guvcview uvcdynctrl
```

Clone most recent github into a new folder [ to not overwrite any changes you may have made ]
```bash
git clone https://github.com/Crall-Lab/DigitalEcology.git /home/pi/DigitalEcologyDL/
```

Check camera acquisition parameters
A Guided User Interface (GUI) should appear that allows you to explore the USB-camera's image acquistion parameters. Once you exit, those settings will be saved. You can restore the default settings through "settings>hardware defaults"
```bash
guvcview
```

# Start video stream and display inference from deep learning models

Running an image classifier [ mobilenetv3 trained on ImageNet dataset ]
```bash
cd /home/pi/DigitalEcologyDL/MiniProject3/
python3 streamDLmodel.py
```

Change the resolution of the video stream 
```bash
cd /home/pi/DigitalEcologyDL/MiniProject3/
python3 streamDLmodel.py -r medium
```

```bash
cd /home/pi/DigitalEcologyDL/MiniProject3/
python3 streamDLmodel.py -r large
```

Running an image object detection model [ efficientDet1 trained on COCO dataset ]
```bash
cd /home/pi/DigitalEcologyDL/MiniProject3/
python3 streamDLmodel.py -d
```

Running an image object detection model [ efficientDet1 trained on COCO dataset ]
and update the detection threshold to see how accuracy changes
```bash
cd /home/pi/DigitalEcologyDL/MiniProject3/
python3 streamDLmodel.py -d -t 0.75
```

Running an image object detection model [ efficientDet1 trained on birds from iNaturalist ]
```bash
cd /home/pi/DigitalEcologyDL/MiniProject3/
python3 streamDLmodel.py -d -b
```

Running an image object detection model over a prerecorded video [ efficientDet1 trained on birds from iNaturalist ]
```bash
cd /home/pi/DigitalEcologyDL/MiniProject3/
python3 streamDLmodel.py -d -b -v
```
# Images and detection data are saved to /home/pi/Documents/detections/$date/

