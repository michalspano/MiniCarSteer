#!/bin/bash

# Run the produced docker image in the environment
# FIXME: currently unused, optimize for the `Python` environment.
docker run --rm -ti --net=host --ipc=host -e DISPLAY=$DISPLAY \
           -v /tmp:/tmp read_car_data:latest --turns-only