# Object Detection API

Simple ML project based on the YOLO network. Built with Flask.

## Getting started

On Ubuntu run:
```
git clone https://github.com/roszcz/yolo-api.git
cd yolo-api
sudo ./run.sh
```

Use:
```
sudo docker-compose stop
sudo docker-compose start
```
to start or stop the application.

To run outside the container run:
```
pipenv install
pipenv run python main.py
```

### Prerequisites

You need [docker](https://docs.docker.com/install/) and [YOLO](https://pjreddie.com/darknet/yolo/) weights (those will be downloaded when using the `run.sh` script).
For development you can use [pipenv](https://pipenv.readthedocs.io/en/latest/).
