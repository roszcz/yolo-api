#!/usr/bin/env bash
echo "Downloading yolov3 weights"
mkdir weights
wget -O yolo/yolov3.weights https://pjreddie.com/media/files/yolov3.weights
