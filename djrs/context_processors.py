"""
Context Processors to add standard RS status into the mix.
"""

from webrs.harness import getWebHarnessGroup
import rs_logging as logging

def pyrs_status(request):
    "Returns context variables for basic status."

    context_extras = {}
    if 'offline' == request.session.get('djrs','offline'):
        return context_extras

    with getWebHarnessGroup(request) as harness:
    
        # default False...     
        pyrs_status = {'connected':False}
    
        if harness is None:
            # major error - bail out.
            context_extras['pyrs_status'] = pyrs_status
            return context_extras
    
        try:
            # run requests (System Status)
            (req_id, msg_id) = harness.request_system_status()
            resp = harness.specific_response(req_id)
            pyrs_status['connection'] = harness.connect_state()
    
            if resp:
                (resp_id, resp_msg) = resp
    
                pyrs_status['connected'] = True
    
                pyrs_status['no_peers'] = resp_msg.no_peers
                pyrs_status['no_connected'] = resp_msg.no_connected
                pyrs_status['upload_rate'] = resp_msg.bw_total.up
                pyrs_status['download_rate'] = resp_msg.bw_total.down
                pyrs_status['network_status'] = resp_msg.net_status  # This will need to be translated
            else:
                pyrs_status['connected'] = False
        except Exception, e:
            logging.info("djrs::context_processors.pyrs_status() Exception: %s" % e)
            pass
    

    # log into rs, via pyrs, and extract all the data.

    # stage 2:
    # get login details from session storage.
    # 

    context_extras['pyrs_status'] = pyrs_status
    return context_extras


def djrs_refresh(request):
    "Returns refresh data"

    context_extras = {}
    if 'offline' == request.session.get('djrs','offline'):
        return context_extras

    #############################################################
    # Handle refresh parameters.
    is_refresh = request.GET.get('refresh', None)
    if is_refresh is not None:
        count = request.session.get('count','0')
    	request.session['count'] = count + 1
    else:
    	request.session['count'] = 0
 
    djrs_refresh = {
	'active' : ('on' == request.session.get('refresh_mode','off')), 
    	'timeout': request.session.get('timeout','30'),
        'count'  : request.session.get('count','0'),
        'url'    : request.path,
    }

    context_extras['djrs_refresh'] = djrs_refresh
    return context_extras


