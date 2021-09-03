#!/bin/bash
echo "###################################################"
echo "#      Start building application image           #"
echo "###################################################"
docker-compose build
echo "###################################################"
echo "#    Application image successfully CREATED.      #"
echo "###################################################"
echo "###################################################"
echo "## Trying to start docker compose infrastructure. #"
echo "###################################################"
docker-compose up -d
echo "###################################################"
echo "#    INFRASTRUCTURE SUCCESSFULLY STARTED          #"
echo "###################################################"