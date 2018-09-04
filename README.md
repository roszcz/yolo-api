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

### Example
```
import requests
response = requests.post(
    'http://0.0.0.0/objects',
    json={
    'url': 'https://cdn.filestackcontent.com/5IkgQW1tS56RAXPnLlFG'
    }
)

response.json()
```

You should get:
```
{
    "objects": [
        {
            "bounding_box": {
                "h": 42,
                "w": 29,
                "x": 439,
                "y": 354
            },
            "confidence": 97,
            "object": "person"
        },
        {
            "bounding_box": {
                "h": 22,
                "w": 22,
                "x": 496,
                "y": 372
            },
            "confidence": 87,
            "object": "person"
        },
        {
            "bounding_box": {
                "h": 435,
                "w": 349,
                "x": 261,
                "y": 23
            },
            "confidence": 79,
            "object": "boat"
        }
    ]
}
```
