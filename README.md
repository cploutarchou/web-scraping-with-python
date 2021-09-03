# stackoverflow-scraper-using-python
A simple scraper app for StackOverflow using MongoDB.

## How to Run
* For the first time you need to run ./init.sh
* You can stop the infrastructure usinf ./stop.sh 
* You can start the infrastructure usinf ./start.sh
## Requirements:
* docker
* docker-compose


## Graylog :
* http://172.21.0.35:9000/
* Usename : admin
* password : admin

To be able to receives application log to Graylog you need to make the followings
1. Create one GelfTCP input stream
   1. Click on System/inputs/gelf
   2. Select Gelf TCP from the dropdown 
   3. Click on Launch new input 
   4. Just add a Title for the input 
   5. Click save
   6. Now you can access application log by Click on Show Received Messages

## Application UI:
* Url : http://172.21.0.25

## MongoDB
* Url : http://172.21.0.20
* Database name : webscrapper
* Database User : admin
* Database password : admin

## Cron JOB:
if is required to update cron job run you can edit the followings:
* Docker/scripts/entrypoint.sh and update the default expression (*/30 * * * *) bases on your requirements.
* Docker/scripts/scheduler.txt and update the default expression (*/30 * * * *) bases on your requirements.


## Important notes
* The application by default fetch the first 10 pages from StackOverflow every 30 minutes.
A cron job run the scraper and update the application database.

* If is required to fetch more pages you can update the passed parameters of method execute_job() from 10 to any other 
value between 10 and 1000 the file in located on app/scraper.py