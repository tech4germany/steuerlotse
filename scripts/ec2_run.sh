#!/bin/bash
cd /home/ubuntu/prod;
sudo docker-compose build;
sudo docker-compose down;
sudo docker-compose up -d;
