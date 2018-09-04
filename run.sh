#!/usr/bin/env bash
if [ ! -f ./yolo/yolov3.weights ]; then
    echo "YOLO Weights not found! Downloading ..."
	wget -O yolo/yolov3.weights https://pjreddie.com/media/files/yolov3.weights
fi

docker-compose build
docker-compose up -d
