#! /usr/bin/bash
sudo systemctl restart arewacinema.start.gunicorn.service
echo "Video On Demand Gunicorn Service Restarted"

sudo systemctl restart nginx.service
echo "Nginx Gunicorn Service Restarted"
