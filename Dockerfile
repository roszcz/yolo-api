FROM ubuntu:16.04
RUN apt-get update

## Pyton installation ##
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev yasm libopencore-amrnb-dev libopencore-amrwb-dev libv4l-dev libxine2-dev
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y libsm6 libxext6 libxrender-dev

## make a local directory
RUN mkdir /yolo_app

# set "counter_app" as the working directory from which CMD, RUN, ADD references
WORKDIR /yolo_app

# now copy all the files in this directory to /counter_app
ADD . .

# wtf
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# pip install the local requirements.txt
RUN pip3 install pipenv
RUN pipenv install

# RUN sh download_models.sh

# Listen to port 5000 at runtime
EXPOSE 5000

# Define our command to be run when launching the container
CMD ["pipenv", "run", "python", "main.py"]
