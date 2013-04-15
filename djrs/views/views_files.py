
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
from webrs.templatize import files_sharedirlist

def file_listing(request, peer_id='', path=''):
    logging.info("djrs.view.file_listing() peer_id: %s, path: %s " % (peer_id, path))

    harness = getWebHarness()
    if harness.is_connected() is False:
        return HttpResponseRedirect(reverse('djrs_login'))

    if path and path[0] != '/':
        # need to have starting /
        path = '/' + path

    template_vars = {}
    try:
        (req_id, msg_id) = harness.request_dirlisting(peer_id, path)
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp
            dict_msg = protobuf_to_dict(resp_msg)
            template_vars['file_listing'] = files_sharedirlist(dict_msg)

    except Exception, e:
        logging.info("Unexpected Exception: %s" % (e))

    return render_to_response('djrs_file_listing.dtml', template_vars, context_instance=RequestContext(request))


