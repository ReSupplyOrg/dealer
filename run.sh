#!/bin/sh

python3 backend/manage.py migrate
python3 backend/manage.py runserver