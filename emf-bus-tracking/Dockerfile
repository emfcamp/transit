FROM python:3.11

ARG DOCKER_GID=996

RUN groupadd -g ${DOCKER_GID} docker \
    &&  useradd -u 1000 -m -s /bin/bash app \
    && usermod -aG docker app

RUN mkdir /app
WORKDIR /app
RUN pip install -U pip

COPY requirements.txt /app/
RUN pip install -r requirements.txt

USER app:docker

COPY . /app

CMD [ "/app/entrypoint.sh" ]