#!/bin/bash

# Run the produced docker image in the environment,
# create a volume in X11-unix to provide display, relay command-line
# arguments (with $@) to the docker container.
docker run --rm -ti --net=host --ipc=host -e DISPLAY=$DISPLAY \
           -u=$(id -u $USER):$(id -g $USER) \
           -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
           -v /tmp:/tmp read_car_data:latest $@
