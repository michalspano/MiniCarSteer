#!/bin/bash

# Launch the OpenH264 Decoder
docker run --rm -ti --net=host --ipc=host -e DISPLAY=$DISPLAY \
                    -v /tmp:/tmp h264decoder:v0.0.5 --cid=253 --name=img
