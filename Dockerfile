FROM python:3.11.9-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    cron && \
    apt-get autoremove -y &&\
    apt-get clean -y

ARG DJANGO_ENV
ENV DJANGO_ENV=${DJANGO_ENV}
RUN echo "Build environment: ${DJANGO_ENV}"

COPY requirements requirements
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements/${DJANGO_ENV}.txt

WORKDIR /app/mepa-api
COPY ./ ./

COPY cronjob/cronjob /etc/cron.d/mec-cron
RUN chmod -R 755 /etc/cron.d/mec-cron && \
    /usr/bin/crontab /etc/cron.d/mec-cron

CMD ["cron", "-f"]
