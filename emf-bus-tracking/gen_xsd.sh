#!/usr/bin/env bash

xsdata generate hafas/rest-2.32.xsd --package hafas.hafas_rest
xsdata generate -r darwin/push-port-xsd --package darwin.push_port