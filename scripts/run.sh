#!/bin/bash

# Run the produced docker image in the environment, relay command-line
# arguments (with $@) to the docker container.
docker run --rm -ti --net=host --ipc=host \
           -e DISPLAY=$DISPLAY \
           -v /tmp:/tmp \
           -u=$(id -u $USER):$(id -g $USER) \
           -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
           -v $(pwd)/src:/app \
           read_car_data:latest $@