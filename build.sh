#!/bin/bash
sudo docker stop ritz

sudo docker rm ritz

sudo docker build -t ritzbot .

sudo docker run \
--name ritz \
--mount type=bind,source=/home/luke/projects/discordbot/ritzbot/logs,target=/usr/src/app/logs/ \
--restart=always \
ritzbot
