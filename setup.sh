#!/bin/bash

# Download weight file

cd ./API/app/model_params
curl --retry-all-errors http://ourcustomers.be/best_weights.pt -o best_weights.pt
cd ..
cd ..

# Create image for API container
docker image build . -t obj_detect_api_image:latest
cd ..

# Create image for Front Office web app container
cd ./webapp
docker image build . -t obj_detect_webapp_image:latest
cd ..

# Launch docker-compose
docker-compose up -d
