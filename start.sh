#!/bin/bash

# run image
docker run --name check-free-space --rm \
-v /var/log/:/var/log \
-it registry.gitlab.com/invisible_bits/docker/check-free-space-disk:latest

# build image
# docker build -t check-free-space:v1.0.0 .