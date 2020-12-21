FROM ubuntu:latest
RUN apt-get update
RUN apt-get -q -y install curl zip unzip git
RUN curl -O -J -L -u ae4e379cc067812bf4e1130cb86d726e5f32de00:x-oauth-basic https://github.com/NeoIsALie/ht-poker/archive/main.zip
RUN unzip ht-poker-main.zip
WORKDIR /ht-poker-main
RUN chmod +x prepare.sh
RUN chmod +x run.sh
