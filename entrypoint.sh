#!/bin/bash
set -e

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createsuperuser_custom

exec "$@"
