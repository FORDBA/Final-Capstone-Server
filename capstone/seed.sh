#!/bin/bash

rm -rf capstoneapi/migrations
rm db.sqlite3
python manage.py makemigrations capstoneapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata workflowusers
python manage.py loaddata companies
python manage.py loaddata states
python manage.py loaddata statuses
python manage.py loaddata workflows
python manage.py loaddata notes
python manage.py loaddata tokens

