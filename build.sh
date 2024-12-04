#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python backendML/manage.py collectstatic --no-input

# Run migrations
python backendML/manage.py makemigrations
python backendML/manage.py migrate
