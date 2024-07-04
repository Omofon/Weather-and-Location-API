#!/bin/bash

# Install pip for Python 3.9
python3.9 -m ensurepip --upgrade

# Install dependencies
python3.9 -m pip install -r requirements.txt

# Collect static files (if you had any)
# python3.9 manage.py collectstatic --noinput
