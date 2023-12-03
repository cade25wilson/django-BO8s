#!/bin/bash
gunicorn --timeout 180 mysite.wsgi &
celery -A mysite worker -l info
