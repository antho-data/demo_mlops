#!/bin/bash

# Delete our images except the API base image

docker image rm --force postgres:11.6-alpine
docker image rm --force obj_detect_api_image:latest
docker image rm --force obj_detect_webapp_image:latest
