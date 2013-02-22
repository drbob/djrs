"""
  RS Auth Middleware
"""

from django.conf import settings

# Django.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Libs.
import rs_logging as logging
from webrs.harness import getWebHarness

class DjRsAuthMiddleware(object):
    """
    Middleware which checks:
	- if webharness is active and logged in.
	- if session is the same.
    """

    def process_request(self, request):
        logging.warning("DjRsAuthMiddleware::process_request() url: %s" % request.get_full_path())
        logging.warning("DjRsAuthMiddleware::process_request() path: %s" % request.path)

        request.session['djrs'] = 'offline'
        if request.path == reverse('djrs_busy'):
            logging.warning("DjRsAuthMiddleware::process_request() Going to Busy Anyway")
            return None

        harness = getWebHarness()
        request.session.modified = True
        session_key = request.session.session_key
        active_session = harness.active_session()

        logging.warning("DjRsAuthMiddleware::process_request() active_session: %s" % active_session)
        logging.warning("DjRsAuthMiddleware::process_request() user_session: %s" % session_key)

        if active_session:
            if active_session == session_key:
                logging.warning("DjRsAuthMiddleware::process_request() Session Active and OK")
            else:
                logging.warning("DjRsAuthMiddleware::process_request() Session Invalid => Busy View")
                return HttpResponseRedirect(reverse('djrs_busy'))

        # if webharness is connected, get session id.
        if harness.is_connected() is False or not active_session:
            logging.warning("DjRsAuthMiddleware::process_request() Not Connected or Active")

            # if they are going to login -> let them through.
            if request.path == reverse('djrs_login'):
                logging.warning("DjRsAuthMiddleware::process_request() Going to Login Anyway")
                return None
               
            logging.warning("DjRsAuthMiddleware::process_request() Redirect to login")
            return HttpResponseRedirect(reverse('djrs_login'))

        logging.warning("DjRsAuthMiddleware::process_request() Is Connected")
        harness.keep_session_current()
        request.session['djrs'] = 'online'
        return None


    #def process_view(self, request, view_func, view_args, view_kwargs):
    #    logging.warning("DjRsAuthMiddleware::process_view()")
    #    return None


    #def process_response(self, request, response):
    #    logging.warning("DjRsAuthMiddleware::process_response()")
    #    return response



