#!/usr/bin/env bash

python3 manage.py collectstatic --noinput || exit 1
python3 manage.py migrate || exit 1

exec gunicorn -w 4 -b [::]:8000 --forwarded-allow-ips \* --access-logfile - --log-level=info --timeout=90 emf_bus_tracking.wsgi:application