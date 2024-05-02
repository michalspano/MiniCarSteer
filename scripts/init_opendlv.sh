#!/bin/bash

# Launch the OpenDLV Vehicle View microservice
docker run --rm -i --init --net=host --name=opendlv-vehicle-view \
           -v $PWD:/opt/vehicle-view/recordings \
           -v /var/run/docker.sock:/var/run/docker.sock \
           -p 8081:8081 chrberger/opendlv-vehicle-view:v0.0.64

