#!/bin/bash
docker stop ritz

docker rm ritz

docker build -t ritzbot .

docker run \
--name ritz \
--mount type=bind,source=/home/luke/projects/discordbot/logs,target=/usr/src/app/logs/ \
ritzbot
