FROM ubuntu:latest
MAINTAINER lumbric@gmail.com

# install requirements
RUN apt-get update && apt-get -y install cron
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

# install lunchbot
COPY . /tmp/lunchbot
COPY config/secrets.yml /etc/lunchbot/
WORKDIR /tmp/lunchbot
RUN python3 setup.py install

# add crontab
ADD config/crontab /etc/cron.d/lunchbot
RUN chmod 0644 /etc/cron.d/lunchbot
RUN crontab /etc/cron.d/lunchbot

RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log
