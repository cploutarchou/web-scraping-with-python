#!/bin/bash

# Start the run once job.
echo "Docker container has been started"
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

export FLASK_APP=/app/main.py
nohup python -m flask run -p 80 --host=0.0.0.0 > log.txt 2>&1 &

# Setup a cron schedule
echo "*/30 * * * * python3 /app/scraper.py 2>&1
# This extra line makes it a valid cron" > scheduler.txt
echo "Start cron schedule"
crontab scheduler.txt
cron -f
