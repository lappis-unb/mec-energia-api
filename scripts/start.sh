#!/bin/bash

echo "${C}____________________________________________________________________________________________________________________________${E}"
echo "${C}=> STARTING CRON                                                                                                            ${E}"
echo 'Cronjobs mec-cron in operating system'
/bin/cp /home/dev/mec-energia-api/cronjob/cronjob /etc/cron.d/mec-cron
crontab /etc/cron.d/mec-cron
cron


./manage.py makemigrations

./manage.py migrate

./manage.py runserver "0.0.0.0:${API_PORT}"
