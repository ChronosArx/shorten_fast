#!/bin/sh

echo 'Running collect static files...'
python manage.py collectstatic --no-input

echo 'Applying migrations...'
python manage.py migrate

echo 'Running server...'
gunicorn shorten_fast.wsgi:application --bind 0.0.0.0:8000
