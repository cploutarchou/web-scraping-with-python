#!/bin/bash
echo "##########################################################################"
echo "#               Start building application image                         #"
echo "##########################################################################"
docker-compose build
echo "##########################################################################"
echo "#             Application image successfully CREATED.                    #"
echo "##########################################################################"
echo "##########################################################################"
echo "#          Trying to start docker compose infrastructure.                #"
echo "##########################################################################"
docker-compose up -d
echo "##########################################################################"
echo "#              INFRASTRUCTURE SUCCESSFULLY STARTED                       #"
echo "##########################################################################"
echo "##########################################################################"
echo "#               Starting process config mongodb servers                  #"
echo "##########################################################################"
sleep 20
docker-compose exec -T mongodb sh -c "mongo -u admin -p admin < /scripts/init_db.js"
echo "##########################################################################"
echo "#            mongodb servers successfully configured                     #"
echo "##########################################################################"
echo "##########################################################################"
echo "#               Starring  scraper for initial load                       #"
echo "##########################################################################"
docker-compose exec -T flask sh -c "python3 /app/scraper.py"
echo "##########################################################################"
echo "#     Initial load complete. Your can now stat used the application.     #"
echo "##########################################################################"
