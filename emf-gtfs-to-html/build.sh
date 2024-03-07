#!/usr/bin/env bash

docker buildx build --platform linux/amd64 --push -t "theenbyperor/emf-gtfs-to-html:latest" .
