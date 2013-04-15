
# Python.

# Django.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse

# Apps
from djrs.forms import SearchForm

# Libs.
import rs_logging as logging
from webrs.harness import getWebHarness

from protobuf_to_dict import protobuf_to_dict
from webrs.templatize import search_searchlist

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
	limit = 500
        (req_id, msg_id) = harness.request_search_list(None, limit)
        resp = harness.specific_response(req_id)
        if resp:
            (resp_id, resp_msg) = resp
            dict_msg = protobuf_to_dict(resp_msg)
            template_vars['search_list'] = search_searchlist(dict_msg['searches'])

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
            dict_msg = protobuf_to_dict(resp_msg)
            template_vars['search_list'] = search_searchlist(dict_msg['searches'])


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


