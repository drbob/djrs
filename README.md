djrs
====

Django based Web Interface to Retroshare


Development Setup
===================

check out the code:

    git clone git://github.com/drbob/djrs.git djrs
    cd djrs
    git submodule update --init


Install the python requirements:
 - django (1.4.X)       (Web Framework)
 - paramiko (>=1.9.0)   (python SSH client)
 - flup                 (python fastcgi interface)
 - protobuf (2.4.1)     (googles serialisation protocol)
     - pycrypto >=2.1

This can be done by running 

    pip install -r djrs_requirements.txt

Launch the development server

    python manage.py runserver

Then point your browser at 127.0.0.0:8000

Finally, you have to launch retroshare-nogui in SSH mode.
This is documented else where (or will be soon).


Running As Production Web Interface.
=============================
(This is not recommended at the moment).

In djrs.settings:

Change the SECRET_KEY

Specify STATIC_ROOT for your Production System.

Setup an external face https server. (nginx, apache, etc)
Be sure to use https, as you will be logging in via this interface.

Launch the fastcgi python interface via the ./run.sh script.


Notes
==========

This is in early development, and not recommended for Internet facing sites yet.
It currently must be run in a "single user" mode

The DjRS webserver and Retroshare nodes do not have to 
be on the same computer, BUT you need to know the IP Address of 
the Retroshare Node in order to login!









