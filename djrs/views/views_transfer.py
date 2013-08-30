
# Python.

# Django.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse

# Libs.
import rs_logging as logging
from webrs.harness import getWebHarness

from protobuf_to_dict import protobuf_to_dict
from webrs.templatize import files_transferlist


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
            dict_msg = protobuf_to_dict(resp_msg)
            if 'transfers' in dict_msg:
                template_vars['upload_list'] = \
                        files_transferlist(dict_msg['transfers'])

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    try:
        (req_id, msg_id) = harness.request_transfer_list(False) # download
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp
            dict_msg = protobuf_to_dict(resp_msg)
            if 'transfers' in dict_msg:
                template_vars['download_list'] = \
                        files_transferlist(dict_msg['transfers'])


    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    return render_to_response('djrs_transfers.dtml', template_vars, context_instance=RequestContext(request))

def transfer_download(request, hash):
    logging.info("djrs.view.transfer_download")

    template_vars = {}
    # parse the extra arguments for the full download details.
    size = request.GET.get('size', None)
    name = request.GET.get('name', None)

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    if not size or not name:
        template_vars['error_message'] = 'Missing Arguments for Download Request'
        return render_to_response('djrs_error.dtml', template_vars, context_instance=RequestContext(request))

    try:
        (req_id, msg_id) = harness.request_transfer_download(hash, name, size)
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


