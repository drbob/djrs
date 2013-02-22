
# Python.

# Django.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse

# Apps
from .forms import LoginForm, SearchForm

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

#def login(request):
#    return render_to_response('djrs_login.dtml', {}, context_instance=RequestContext(request))
#

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


def friends(request):
    logging.info("djrs.view.friends")

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    template_vars = {}
    try:
        (req_id, msg_id) = harness.request_peer_list("all")
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp
            template_vars['friend_list'] = resp_msg.peers

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    return render_to_response('djrs_friends.dtml', template_vars, context_instance=RequestContext(request))

def friend_details(request, friend_id):
    logging.info("djrs.view.friend_details")

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    template_vars = {}
    try:
        (req_id, msg_id) = harness.request_peer_list("all")
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp
            template_vars['friend_list'] = resp_msg.peers

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    return render_to_response('djrs_friend_details.dtml', template_vars, context_instance=RequestContext(request))

def apps(request):
    return render_to_response('djrs_apps.dtml', {}, context_instance=RequestContext(request))

def about(request):
    return render_to_response('djrs_about.dtml', {}, context_instance=RequestContext(request))

def transfers(request):
    logging.info("djrs.view.transfers")

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    template_vars = {}
    try:
        (req_id, msg_id) = harness.request_transfer_list(True) # upload
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp
            template_vars['upload_list'] = resp_msg.transfers

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    try:
        (req_id, msg_id) = harness.request_transfer_list(False) # download
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp
            template_vars['download_list'] = resp_msg.transfers

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    return render_to_response('djrs_transfers.dtml', template_vars, context_instance=RequestContext(request))

def transfer_download(request, hash):
    logging.info("djrs.view.transfer_download")

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    template_vars = {}
    try:
        (req_id, msg_id) = harness.request_transfer_download(hash)
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    # just redirect to general display.
    return HttpResponseRedirect(reverse('djrs_transfers'))


def transfer_cancel(request, hash):
    logging.info("djrs.view.transfer_cancel")

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    template_vars = {}
    try:
        (req_id, msg_id) = harness.request_transfer_cancel(hash)
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    # just redirect to general display.
    return HttpResponseRedirect(reverse('djrs_transfers'))


def transfer_pause(request, hash):
    logging.info("djrs.view.transfer_pause")

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    template_vars = {}
    try:
        (req_id, msg_id) = harness.request_transfer_pause(hash)
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    # just redirect to general display.
    return HttpResponseRedirect(reverse('djrs_transfers'))


def searches(request):
    logging.info("djrs.view.searches")

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    template_vars = {}

    if request.method == 'POST': # If the form has been submitted...
        form = SearchForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass

            terms = form.cleaned_data['terms']
            term_list = terms.split(' ')

            logging.info("Completed Search Form. Term_list: %s" % term_list)

            # default...
            template_vars['search_started'] = False
            try:
                # trigger the search...

                (req_id, msg_id) = harness.request_basic_search(term_list)
                resp = harness.specific_response(req_id)
                if resp:
                    (resp_id, resp_msg) = resp
                    template_vars['search_started'] = True
                    template_vars['search_terms'] = term_list

            except Exception, e:
                logging.info("Unexpected Exception: %s" % (e))

            # reset the form for next search.
            # form = SearchForm() # An unbound form
            form = None # disable for more info,
        else:
            # invalid form will return errors.
            pass
    else:
        form = SearchForm() # An unbound form

    template_vars['form'] = form

    # now grab existing search results.
    try:
        (req_id, msg_id) = harness.request_search_list(None)
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp
            template_vars['search_list'] = resp_msg.searches

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    return render_to_response('djrs_search.dtml', template_vars, context_instance=RequestContext(request))


def search_details(request, search_id):
    logging.info("djrs.view.search_details")

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    template_vars = {}
    try:
        (req_id, msg_id) = harness.request_search_list(int(search_id))
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp
            template_vars['search_list'] = resp_msg.searches

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    return render_to_response('djrs_search.dtml', template_vars, context_instance=RequestContext(request))


def search_close(request, search_id):
    logging.info("djrs.view.search_close")

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    template_vars = {}
    try:
        (req_id, msg_id) = harness.request_close_search(int(search_id))
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    # just redirect to general display.
    return HttpResponseRedirect(reverse('djrs_searches'))



def chat(request):
    logging.info("djrs.view.chat")

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    template_vars = {}
    try:
        (req_id, msg_id) = harness.request_chat_lobby_list("all")
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp
            template_vars['lobby_list'] = resp_msg.lobbies

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    return render_to_response('djrs_chat.dtml', template_vars, context_instance=RequestContext(request))

def chat_friend(request, friend_id):
    return render_to_response('djrs_chat_friend.dtml', {}, context_instance=RequestContext(request))

def chat_lobby(request, lobby_id):
    return render_to_response('djrs_chat_lobby.dtml', {}, context_instance=RequestContext(request))


