
# dependancies for this server.
import os, sys
import django.core.handlers.wsgi
from tornado import httpserver, ioloop, wsgi
from tornado.web import Application, StaticFileHandler, FallbackHandler

import djrs_path
#from djrs_path import app_dir

os.environ['DJANGO_SETTINGS_MODULE'] = 'djrs.settings'

# explicit dependencies for django + app.
import djrs_deps
 
def runserver():
    #static_path = os.path.join(app_dir, 'static')
    static_path = os.path.join('.', 'static')
 
    wsgi_app = wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
    tornado_app = Application([
        (r'/static/(.*)', StaticFileHandler, {'path': static_path}),
        ('.*', FallbackHandler, dict(fallback=wsgi_app)),
    ])
    server = httpserver.HTTPServer(tornado_app)
    server.listen(8000)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        sys.exit(0)
 
if __name__ == '__main__':
    runserver()

