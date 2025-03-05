FROM python:3.9-buster
LABEL MAINTAINER="Raj Jagtap <raj.jagtap.17003@iitgoa.ac.in>"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

RUN apt-get update && apt-get install -y \
wget unzip curl \
fonts-liberation \
libatk-bridge2.0-0 \
libatk1.0-0 \
libcups2 \
libdbus-1-3 \
libgdk-pixbuf2.0-0 \
libnspr4 \
libnss3 \
libxcomposite1 \
libxdamage1 \
libxrandr2 \
xdg-utils \
libgbm-dev
   

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

ADD ./requirements.txt /var/www/requirements.txt
RUN pip install --default-timeout=100 -r requirements.txt
ADD . /var/www/
RUN pip install gunicorn

RUN addgroup --gid $GROUP_ID www
RUN adduser --uid $USER_ID --shell /bin/sh --gid $GROUP_ID www 

USER www

EXPOSE 5000

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi:app"]