FROM python:3.9-buster
LABEL MAINTAINER="Raj Jagtap <raj.jagtap.17003@iitgoa.ac.in>"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

RUN apt-get update 
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils
RUN apt-get -qq -y install  libxpm4 libxrender1 libgtk2.0-0 libnss3\ 
       libgconf-2-4  libpango1.0-0 libxss1 libxtst6 fonts-liberation\ 
       libappindicator1 xdg-utils

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

ADD ./requirements.txt /var/www/requirements.txt
RUN pip install -r requirements.txt
ADD . /var/www/
RUN pip install gunicorn

RUN addgroup --gid $GROUP_ID www
RUN adduser --uid $USER_ID --shell /bin/sh --gid $GROUP_ID www 

USER www

EXPOSE 5000

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi:app"]