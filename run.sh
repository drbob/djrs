#!/bin/sh

python manage.py runfcgi host=127.0.0.1 port=8080 daemonize=false max_children=1

