#!/bin/bash
source ../venv/bin/activate
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --log-level info
