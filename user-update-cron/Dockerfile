FROM python:3.9-slim

WORKDIR /src

COPY ./cronjob.py .

RUN apt-get update && apt-get install cron -y
COPY ./cronjob /etc/cron.d/container_cronjob
RUN chmod 0644 /etc/cron.d/container_cronjob
RUN crontab /etc/cron.d/container_cronjob
RUN touch /var/log/cron.log

ENTRYPOINT ["python3", "cronjob.py","&&", "cron", "&&", "tail -f /var/log/cron.log"]