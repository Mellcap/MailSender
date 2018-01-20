FROM python:2.7
MAINTAINER imellcap@gmail.com

ADD . /MailSender/
WORKDIR /MailSender
RUN pip install -r requirements.txt

EXPOSE 5000