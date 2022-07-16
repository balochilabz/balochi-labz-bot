FROM debian:latest

RUN apt update && apt upgrade -y
RUN apt install git curl python3-pip ffmpeg -y
RUN pip3 install -U pip
RUN cd /
RUN git clone https://github.com/balochilabz/balochi-labz-bot
RUN cd balochi-labz-bot
WORKDIR /balochi-labz-bot
RUN pip3 install -U -r requirements.txt
CMD python3 app.py