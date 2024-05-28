#!/bin/bash

# Runs the produced docker image in the docker environment.
# 
# -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
#
# This flag creates a mapping between the host system and
# the docker container. The first part is the directory
# on the host machine and the second part is the directory
# on the container. Then we also specify RW because we want to
# be able to update the GUI (debug window) that is present.
#
# -u=$(id -u $USER):$(id -g $USER) \
#
# To ensure that the container accesses files that are not
# owned by the root user or any other user we explicity 
# specify which user the container should run as.
# The first part: $(id -u $USER) is the user ID, and the second
# part is the group ID. Together they create USERID:GROUPID
# which tells the container which user and group it should run 
# as. We do this to ensure that the docker container runs 
# with plausible privileges.

docker run --rm -ti --net=host --ipc=host -e DISPLAY=$DISPLAY \
           -u=$(id -u $USER):$(id -g $USER) \
           -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
           -v /tmp:/tmp read_car_data:latest $@
