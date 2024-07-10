FROM python:3.10.5

RUN apt-get update && \
apt-get install -y libpq-dev cron

COPY . .
RUN pip install -U --no-cache-dir -r requirements.txt

# ----------------------------------< cron >-----------------------------------------------
COPY cronjob/cronjob /etc/cron.d/mec-cron
RUN chmod -R 755 /etc/cron.d/mec-cron && \
    /usr/bin/crontab /etc/cron.d/mec-cron

WORKDIR /home/dev/mec-energia-api
