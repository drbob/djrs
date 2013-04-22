
# Python.

# Django.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.conf import settings

# Apps
from djrs.forms import LoginForm

# Libs.
import rs_logging as logging
from webrs.harness import getWebHarness

import paramiko

def home(request):
    logging.info("djrs.view.home")
    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))
    return render_to_response('djrs_home.dtml', {}, context_instance=RequestContext(request))

def login(request):

    template_vars = {}

    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            logging.info("Hello... we have a form")

            harness = getWebHarness()

            # try to login.
            # wait around until we are logged in.
            user = form.cleaned_data['user']
            pwd = form.cleaned_data['password']
            host = form.cleaned_data['host']
            port = form.cleaned_data['port']

            try: 
                harness.connect_params(user, pwd, host, port)

                # success! -> save session as active.
                harness.set_session(request.session.session_key)

                # setup 
                harness.setup_connection()

                return HttpResponseRedirect(reverse('djrs_home'))

            except paramiko.SSHException, e:
                logging.info("Login Exception: %s" % (e))
                error_msg = "Login Error: %s" % e
            except Exception, e:
                error_msg = "Unexpected Error: %s" % e
                logging.info("Unexpected Exception: %s" % (e))
            template_vars['error_message'] = error_msg

    else:
        form = LoginForm() # An unbound form

    template_vars['form'] = form
    return render_to_response('djrs_login.dtml', template_vars, context_instance=RequestContext(request))

def apps(request):
    return render_to_response('djrs_apps.dtml', {}, context_instance=RequestContext(request))

def about(request):
    return render_to_response('djrs_about.dtml', {}, context_instance=RequestContext(request))


def busy(request):
    return render_to_response('djrs_busy.dtml', {}, context_instance=RequestContext(request))


def refresh(request):
    # parse the extra arguments for the full download details.
    url = request.GET.get('url', None)
    timeout = request.GET.get('timeout', None)
    count = request.GET.get('count', None)

    return HttpResponseRedirect(url)


def refresh_enable(request):
    request.session['refresh_mode'] = 'on'
    return HttpResponseRedirect(reverse('djrs_home'))

def refresh_disable(request):
    request.session['refresh_mode'] = 'off'
    return HttpResponseRedirect(reverse('djrs_home'))



