# Functions to convert protobuf objects into useful template dictionaries.
# 

# all the msgs.
from pyrs.proto import core_pb2
from pyrs.proto import system_pb2
from pyrs.proto import peers_pb2
from pyrs.proto import chat_pb2
from pyrs.proto import search_pb2
from pyrs.proto import files_pb2

import rs_logging as logging

def dump_dict(addict):

    logging.info("templatize.dump_dict")
    for k, v in addict.iteritems():
        logging.info("K: %s => v: %s" % (k, v))


def core_location(location):
    state = location['state']
    name = 'Unknown'
    if state & core_pb2.Location.CONNECTED:
        name = 'Connected'
    elif state & core_pb2.Location.ONLINE:
        name = 'Online'
    elif state & core_pb2.Location.UNREACHABLE:
        name = 'Unreachable'
        
    location['status'] = name

    return location


def core_person(person):
    relation = person['relation']
    #name = 'Unknown'
    # More sensible default.
    name = 'Friend of Friends'
    if relation == core_pb2.Person.YOURSELF:
        person['self'] = True
        name = 'Self'
    elif relation == core_pb2.Person.FRIEND:
        person['friend'] = True
        name = 'Friend'
    elif relation == core_pb2.Person.FRIEND_OF_MANY_FRIENDS:
        person['fof'] = True
        name = 'Friend of Many Friends'
    elif relation == core_pb2.Person.FRIEND_OF_FRIENDS:
        person['fof'] = True
        name = 'Friend of Friends'
    person['relationship'] = name

    # cleanup locations  
    if 'locations' in person:
        locations = person['locations'] 
        tlocs = []
        for location in locations:
            tlocs.append(core_location(location))
        person['locations'] = tlocs

    return person
        
def core_personlist(person_list):
    tpersons = []
    for person in person_list:
        tpersons.append(core_person(person))
    return tpersons
        

# TRANSFERS.

def nice_file_size(size):
    EXT = ['B', 'KB', 'MB', 'GB', 'TB']

    ext_idx = 0
    while( (ext_idx < len(EXT) - 1) and size > 900):
        size = size / 1000.0
        ext_idx += 1    

    return "%0.1f %s" % (size, EXT[ext_idx])


def files_filetransfer(item):
    item['percentage_done'] = "%0.2f %%" % (item['fraction'] * 100)
    item['size_txt'] = nice_file_size( float(item['file']['size']) )

    return item

def files_transferlist(transfer_list):
    itemlist = []
    for item in transfer_list:
        itemlist.append(files_filetransfer(item))
    return itemlist
        
    
# FILE LISTINGS.

def core_file(item):
    item['size_txt'] = nice_file_size( float(item['size']) )

    return item

def files_sharedirlist(dir_list):

    if 'files' not in dir_list:
        return dir_list

    itemlist = []
    for item in dir_list['files']:
        itemlist.append(core_file(item))
    dir_list['files'] = itemlist
    return dir_list
        




# SEARCHES.

def search_searchhit(item):

    item['size_txt'] = nice_file_size( float(item['file']['size']) )

    name = 'Remote'
    flags = item['loc']
    if flags & search_pb2.SearchHit.LOCAL:
        item['local'] = True
        name = 'Local'
    item['loc_txt'] = name

    return item

def search_searchset(search_set):

    if 'hits' not in search_set:
        return search_set

    itemlist = []
    for item in search_set['hits']:
        itemlist.append(search_searchhit(item))
    search_set['hits'] = itemlist
    return search_set

def search_searchlist(search_list):
    itemlist = []
    for item in search_list:
        itemlist.append(search_searchset(item))
    return itemlist
        

# CHAT    

from datetime import datetime
def chat_chatmessage(item):

    recv = datetime.fromtimestamp(item['recv_time'])
    delta = (datetime.now() - recv).seconds

    item['recv_datetime'] = recv
    item['send_datetime'] = datetime.fromtimestamp(item['send_time'])

    if (delta < 100):
    	item['when'] = "%d secs ago" % int(delta)
    elif (delta < 900):
    	item['when'] = "%d minutes ago" % int(delta / 60)
    elif (delta < 24 * 3600):
        # different formats?
    	item['when'] = recv
    else:
    	item['when'] = recv

    return item

def chat_chathistory(chat_list):
    itemlist = []
    for item in chat_list:
        itemlist.append(chat_chatmessage(item))
    return itemlist
        
