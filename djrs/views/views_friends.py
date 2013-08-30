
# Python.

# Django.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse

# Libs.
import rs_logging as logging
from protobuf_to_dict import protobuf_to_dict
from webrs.harness import getWebHarness

from webrs.templatize import core_personlist


def friends(request, list_type='friends'):
    logging.info("djrs.view.friends")

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    template_vars = {}
    acceptable_types = ['all', 'friends', 'connected', 'self']
    if list_type not in acceptable_types:
        template_vars['error_message'] = 'Invalid Arguments Friends Listing'
        return render_to_response('djrs_error.dtml', template_vars, context_instance=RequestContext(request))

    try:
        (req_id, msg_id) = harness.request_peer_list(list_type)
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp
            dict_msg = protobuf_to_dict(resp_msg)
            if 'peers' in dict_msg:
                template_vars['friend_list'] = core_personlist(dict_msg['peers'])

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    # build a list from Lobby List.
    template_vars['sidebar_menu'] = 'Friend Sets'
    template_vars['sidebar_sublinks'] = [
        { 'url':'/friends/friends/' , 'name': 'Your Friends' },
        { 'url':'/friends/connected/' , 'name': 'Online' },
        { 'url':'/friends/all/' , 'name': 'All Known Peers' },
        { 'url':'/friends/self/' , 'name': 'Yourself' }
    ]

    return render_to_response('djrs_friends.dtml', template_vars, context_instance=RequestContext(request))

def friend_details(request, friend_id):
    logging.info("djrs.view.friend_details")

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    template_vars = {}
    try:
        (req_id, msg_id) = harness.request_peer_details(friend_id)
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp
            dict_msg = protobuf_to_dict(resp_msg)
            if 'peers' in dict_msg:
                template_vars['friend_list'] = core_personlist(dict_msg['peers'])


    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    # build a list from Lobby List.
    template_vars['sidebar_menu'] = 'Friend Sets'
    template_vars['sidebar_sublinks'] = [
        { 'url':'/friends/friends/' , 'name': 'Your Friends' },
        { 'url':'/friends/connected/' , 'name': 'Online' },
        { 'url':'/friends/all/' , 'name': 'All Known Peers' },
        { 'url':'/friends/self/' , 'name': 'Yourself' }
    ]

    return render_to_response('djrs_friend_details.dtml', template_vars, context_instance=RequestContext(request))



def friend_add(request, friend_id):
    logging.info("djrs.view.friend_add")

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    template_vars = {}
    try:
        (req_id, msg_id) = harness.request_friend_add(friend_id, True)
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp
            # should check the result...

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    return HttpResponseRedirect(reverse('djrs_friends'))


def friend_remove(request, friend_id):
    logging.info("djrs.view.friend_remove")

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    template_vars = {}
    try:
        (req_id, msg_id) = harness.request_friend_add(friend_id, False)
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp
            # should check the result...

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    return HttpResponseRedirect(reverse('djrs_friends'))

