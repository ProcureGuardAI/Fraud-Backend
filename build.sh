#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r backendML/requirements.txt

# Collect static files
cd backendML
python manage.py collectstatic --no-input

# Run migrations
python manage.py makemigrations
python manage.py migrate
