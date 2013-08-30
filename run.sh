#!/bin/sh

python manage.py runfcgi host=127.0.0.1 port=8080 \
    daemonize=false maxchildren=1 maxspare=1
 
# maxchildren, maxspare: ensure only one process serves the
# requests; otherwise the session management doesn't work correctly.
