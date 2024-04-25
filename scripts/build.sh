#!/bin/bash

# Build the docker image based on the Dockerfile
# FIXME: currently unused for the `Python` module.
docker build --rm -f Dockerfile -t read_car_data .
