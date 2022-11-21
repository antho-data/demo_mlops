#!/bin/bash

# Delete our containers

docker container rm --force obj_detect_db_users
docker container rm --force obj_detect_db_logs
docker container rm --force obj_detect_api_fo
docker container rm --force obj_detect_api_bo
docker container rm --force obj_detect_webapp_fo
docker container rm --force obj_detect_webapp_bo

