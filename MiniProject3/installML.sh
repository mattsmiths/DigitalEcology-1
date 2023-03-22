#! /bin/bash

sudo apt-get update
sudo apt install python3-numpy
sudo apt install python3-opencv


wget https://tfhub.dev/google/lite-model/imagenet/mobilenet_v3_large_075_224/classification/5/default/1?lite-format=tflite
sudo apt install python3-tflite-runtime libatlas-base-dev
pip3 install --no-deps https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

sudo apt-get install libedgetpu1-std
sudo apt install python3-tflite-runtime libatlas-base-dev
sudo apt install guvcview uvcdynctrl
