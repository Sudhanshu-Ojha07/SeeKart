#!/bin/bash
pip install -r requirements.txt
python3 manage.py collectstatic --noinput --clear
python3 manage.py migrate
