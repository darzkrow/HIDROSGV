#!/bin/bash
source ../venv/bin/activate
celery -A config worker --loglevel=INFO
