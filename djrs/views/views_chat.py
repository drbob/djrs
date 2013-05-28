
# Python.

# Django.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse

# Apps
from djrs.forms import ChatForm

# Libs.
import rs_logging as logging
from webrs.harness import getWebHarnessGroup
from pyrs.proto import chat_pb2

from protobuf_to_dict import protobuf_to_dict
from webrs.templatize import chat_chathistory

def chat(request):
    logging.info("djrs.view.chat")

    with getWebHarnessGroup(request) as harness:
        if harness.is_connected() is False:
            return HttpResponseRedirect(reverse('djrs_login'))
    
        template_vars = {}
        try:
            (req_id, msg_id) = harness.request_chat_lobby_list("all")
            resp = harness.specific_response(req_id)
            if resp:
                (resp_id, resp_msg) = resp
                template_vars['lobby_list'] = resp_msg.lobbies
    
                # build a list from Lobby List.
                template_vars['sidebar_menu'] = 'Subscribed Lobbies'
                template_vars['sidebar_sublinks'] = []
                for lobby in resp_msg.lobbies:
                    if lobby.lobby_state == chat_pb2.ChatLobbyInfo.LOBBYSTATE_JOINED:
                        url = "/lobby/%s/" % lobby.lobby_id
                        template_vars['sidebar_sublinks'].append({ 'url':url , 'name': lobby.lobby_name })
    
        except Exception, e:
            logging.info("Unexpected Exception: %s" % (e))
    
    return render_to_response('djrs_chat.dtml', template_vars, context_instance=RequestContext(request))




def lobby_join(request, lobby_id):
    logging.info("djrs.view.lobby_join")
    template_vars = {}

    with getWebHarnessGroup(request) as harness:
        if harness.is_connected() is False:
            return HttpResponseRedirect(reverse('djrs_login'))
    
        try:
            (req_id, msg_id) = harness.request_join_or_leave_lobby(lobby_id, True)
            resp = harness.specific_response(req_id)
            if resp:
                (resp_id, resp_msg) = resp
    
        except Exception, e:
            logging.info("Unexpected Exception: %s" % (e))
    
    # just redirect to general display.
    return HttpResponseRedirect(reverse('djrs_chat'))


def lobby_drop(request, lobby_id):
    logging.info("djrs.view.lobby_drop")
    template_vars = {}

    with getWebHarnessGroup(request) as harness:
        if harness.is_connected() is False:
            return HttpResponseRedirect(reverse('djrs_login'))
    
        try:
            (req_id, msg_id) = harness.request_join_or_leave_lobby(lobby_id, False)
            resp = harness.specific_response(req_id)
            if resp:
                (resp_id, resp_msg) = resp
    
        except Exception, e:
            logging.info("Unexpected Exception: %s" % (e))

    # just redirect to general display.
    return HttpResponseRedirect(reverse('djrs_chat'))


def chat_lobby(request, lobby_id):
    logging.info("djrs.view.chat_lobby")
    template_vars = {}
    template_vars['lobby_id'] = lobby_id

    with getWebHarnessGroup(request) as harness:
        if harness.is_connected() is False:
            return HttpResponseRedirect(reverse('djrs_login'))
    
        # get this lobby details.
        try:
            (req_id, msg_id) = harness.request_chat_lobby_list("all")
            resp = harness.specific_response(req_id)
            if resp:
                (resp_id, resp_msg) = resp
                for lobby in resp_msg.lobbies:
                    if lobby.lobby_id == lobby_id:
                        template_vars['lobby_details'] = lobby
        
                # build a list from Lobby List.
                template_vars['sidebar_menu'] = 'Subscribed Lobbies'
                template_vars['sidebar_sublinks'] = []
                for lobby in resp_msg.lobbies:
                    if lobby.lobby_state == chat_pb2.ChatLobbyInfo.LOBBYSTATE_JOINED:
                        url = "/lobby/%s/" % lobby.lobby_id
                        template_vars['sidebar_sublinks'].append({ 'url':url , 'name': lobby.lobby_name })
    
        except Exception, e:
            logging.info("Unexpected Exception: %s" % (e))

        ## get chat from lobby.
        #try:
        #    (req_id, msg_id) = harness.request_lobby_messages(lobby_id)
        #    resp = harness.specific_response(req_id)
        #    if resp:
        #        (resp_id, resp_msg) = resp
        #        dict_msg = protobuf_to_dict(resp_msg)
        #        template_vars['messages'] = chat_chathistory(dict_msg['msgs'])
        #
        #except Exception, e:
        #    logging.info("Unexpected Exception: %s" % (e))

    form = ChatForm() # An unbound form for submitting messages.
    template_vars['form'] = form

    return render_to_response('djrs_chat_lobby.dtml', template_vars, context_instance=RequestContext(request))

def chat_friend(request, peer_id):
    logging.info("djrs.view.chat_friend")
    template_vars = {}
    template_vars['peer_id'] = peer_id

    with getWebHarnessGroup(request) as harness:
        if harness.is_connected() is False:
            return HttpResponseRedirect(reverse('djrs_login'))
    
        # get peer details.
        # get this lobby details.
        #try:
        #    (req_id, msg_id) = harness.request_chat_lobby_list("all")
        #    resp = harness.specific_response(req_id)
        #    if resp:
        #        (resp_id, resp_msg) = resp
        #        for lobby in resp_msg.lobbies:
        #            if lobby.lobby_id == lobby_id:
        #                template_vars['lobby_details'] = lobby
        #
        #        # build a list from Lobby List.
        #        template_vars['sidebar_menu'] = 'Subscribed Lobbies'
        #        template_vars['sidebar_sublinks'] = []
        #        for lobby in resp_msg.lobbies:
        #            if lobby.lobby_state == chat_pb2.ChatLobbyInfo.LOBBYSTATE_JOINED:
        #                url = "/lobby/%s/" % lobby.lobby_id
        #                template_vars['sidebar_sublinks'].append({ 'url':url , 'name': lobby.lobby_name })
        #
        #except Exception, e:
        #    logging.info("Unexpected Exception: %s" % (e))
    
        # get chat from lobby.
        try:
            (req_id, msg_id) = harness.request_chat_history('friend', peer_id)
            resp = harness.specific_response(req_id)
            if resp:
                (resp_id, resp_msg) = resp
                dict_msg = protobuf_to_dict(resp_msg)
                template_vars['messages'] = chat_chathistory(dict_msg['msgs'])
    
        except Exception, e:
            logging.info("Unexpected Exception: %s" % (e))
    
    form = ChatForm() # An unbound form for submitting messages.
    template_vars['form'] = form

    return render_to_response('djrs_chat_friend.dtml', template_vars, context_instance=RequestContext(request))



def chat_send(request, chat_type, chat_id):
    logging.info("djrs.view.chat_send")

    template_vars = {}


    if request.method == 'POST': 
        form = ChatForm(request.POST) 
        if form.is_valid(): 

            with getWebHarnessGroup(request) as harness:
                message = form.cleaned_data['message']
                # get this lobby details.
                try:
                    (req_id, msg_id) = harness.request_send_message(chat_type,  chat_id, message)
                    resp = harness.specific_response(req_id)
                    if resp:
                        (resp_id, resp_msg) = resp
                except Exception, e:
                    logging.info("Unexpected Exception: %s" % (e))

    else:
        form = ChatForm() # An unbound form

    if chat_type == 'lobby':
        return HttpResponseRedirect(reverse('djrs_chat_lobby', kwargs={'lobby_id':chat_id}))
    else:
        return HttpResponseRedirect(reverse('djrs_chat_friend', kwargs={'peer_id':chat_id}))


