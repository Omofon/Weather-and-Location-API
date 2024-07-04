#!/bin/bash

# Upgrade pip to the latest version
python3.9 -m pip install --upgrade pip

# Install dependencies
python3.9 -m pip install -r requirements.txt

# Apply database migrations
python3.9 manage.py migrate --noinput

# Collect static files (if you had any)
python3.9 manage.py collectstatic --noinput
