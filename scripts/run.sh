#!/bin/bash

# Run the produced docker image in the environment, relay command-line
# arguments (with $@) to the docker container.
docker run --rm -ti --net=host --ipc=host -e DISPLAY=$DISPLAY \
           -v /tmp:/tmp read_car_data:latest $@
