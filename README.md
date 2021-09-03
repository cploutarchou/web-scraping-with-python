# stackoverflow-scraper-using-python
A simple scraper app for StackOverflow using MongoDB.

## How to Run

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


Important notes
The application by default fetch the first 10 pages from StackOverflow every 30 minutes.
A cron job run the scraper and update the application database.

If is required to fetch more pages you can update the passed parameters of method execute_job() from 10 to any other 
value between 10 and 1000 the file in located on app/scraper.py