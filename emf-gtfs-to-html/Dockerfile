FROM node:16

RUN apt update
RUN apt install -y chromium

WORKDIR /

RUN npm -g config set user root
RUN npm install -g gtfs-to-html

COPY config.json /
COPY views /views
COPY static /static
COPY run.sh /

CMD [ "/run.sh" ]