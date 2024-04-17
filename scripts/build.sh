#!/bin/bash

# Build the docker image based on the Dockerfile
docker build --rm -f ../Dockerfile -t read_car_data .
