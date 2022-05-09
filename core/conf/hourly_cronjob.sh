#!/bin/bash
# */30 * * * * /home/arewacinema/video_on_demand/hourly_jobs.sh >> /home/arewacinema/video_on_demand/logs/hourly.log
DJANGODIR=/home/arewacinema/video_on_demand/src
DJANGO_SETTINGS_MODULE=video_on_demand.settings


source /home/arewacinema/video_on_demand/bin/activate
export EMAIL_PASS='ArewaMessages@2022#'
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH


exec /home/arewacinema/video_on_demand/bin/python /home/ubuntu/video_on_demand/src/manage.py runjobs hourly
