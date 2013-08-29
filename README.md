djrs
====

Django based Web Interface to Retroshare


Development Setup
===================

check out the code:

    git clone git://github.com/drbob/djrs.git djrs-code
    cd djrs-code
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

Then point your browser at http://127.0.0.1:8000/

Finally, you have to launch retroshare-nogui in SSH mode.
For instructions about how to do this, see out blog: http://retroshareteam.wordpress.com/2013/01/27/using-retroshare-on-the-excito-bubba3/  there are RPC notes towards the bottom of the page.

There are also notes in Retroshare source code: retroshare-nogui/src/retroshare-nogui.pro


Running via Tornado server.
=============================

This should be as simple as running

    python djrs_server.py

Then point your browser at http://127.0.0.1:8000/

This is the recommended way of running DjRS!


Building into a Standalone App 
=============================

Once you have got the tornado server running, you can *try*
and build the standalone app. This is still work-in-progress.
It has been successfully done a couple of times.

Let us know if it works for you.

    python cxfreeze_setup.py build


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

The recommended method is to setup your rs-nogui node with an forwarded SSH port on your raspberry-PI or dreamplug.
Then run the web app on any other computers when you want to access you node.

The DjRS webserver and Retroshare nodes do not have to 
be on the same computer, BUT you need to know the IP Address of 
the Retroshare Node in order to login!

DjRS is still in early development, and it is not recommended to expose the Web Interface directly to the Internet yet.









