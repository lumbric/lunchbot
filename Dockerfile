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

RUN touch /var/log/cron.log

# no idea why, but as it seems with our current proxmox / LXC setup the crontab command does not
# seem to work when run at build time... Workaround: run it add run time.
CMD crontab /tmp/lunchbot/config/crontab && cron && tail -f /var/log/cron.log
