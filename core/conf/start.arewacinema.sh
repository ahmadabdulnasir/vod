#!/bin/bash

NAME="video_on_demand"
DJANGODIR=/home/arewacinema/video_on_demand/src/ 
SOCKFILE=/home/arewacinema/video_on_demand/src/gunicorn.sock
USER=arewacinema
GROUP=webdata
NUM_WORKERS=1
DJANGO_SETTINGS_MODULE=video_on_demand.settings
DJANGO_WSGI_MODULE=video_on_demand.wsgi

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/arewacinema/video_on_demand/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export EMAIL_HOST_PASSWORD='Pass@1234'
# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /home/arewacinema/video_on_demand/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE
