#!/usr/bin/env bash

cd / && \
gtfs-to-html --configPath /config.json && \
cp -r static/* /html/emf/ && \
exit 0