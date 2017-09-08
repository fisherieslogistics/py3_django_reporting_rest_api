#!/bin/sh
set -e

python3 manage.py migrate --noinput
python3 manage.py loaddata reporting/migrations/data/groups.json
python3 manage.py loaddata reporting/migrations/data/species.json

/usr/local/bin/uwsgi --ini /home/docker/code/uwsgi.ini
