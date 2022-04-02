FROM python:3.9
LABEL MAINTAINER="Raj Jagtap <raj.jagtap.17003@iitgoa.ac.in>"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

ADD ./requirements.txt /var/www/requirements.txt
RUN pip install -r requirements.txt
ADD . /var/www/
RUN pip install gunicorn

RUN addgroup --gid $GROUP_ID www
RUN adduser --uid $USER_ID --shell /bin/sh --gid $GROUP_ID www 

USER www

EXPOSE 5000

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi:app"]