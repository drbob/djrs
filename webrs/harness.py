# Test harness for pyrs.
#
# Sets up everything....
# accepts a bunch of requests.
# then waits for responses, prints them out and ensures 'success'
# 





import pyrs.comms
import pyrs.rpc
import pyrs.msgs
import pyrs.responder

import pyrs.test.auth
import pyrs.test.responders

import time, datetime

import rs_logging as logging


# all the msgs.
from pyrs.proto import core_pb2
from pyrs.proto import system_pb2
from pyrs.proto import peers_pb2
from pyrs.proto import chat_pb2
from pyrs.proto import search_pb2
from pyrs.proto import files_pb2




# The Web Harness has to handle the connections to RS in the background.
# we maintain a single global of this class here....
# it will periodically die, and need to be restarted.


__persistent_WebPyRs = None

def getWebHarness():
    global __persistent_WebPyRs
    if __persistent_WebPyRs is None:
        __persistent_WebPyRs = WebHarness()
    return __persistent_WebPyRs
    

class WebHarness:
  def __init__(self):

    # Construct a Msg Parser.
    self.parser = pyrs.msgs.RpcMsgs();

    # create comms object.
    # dummy connection parameters.
    user = "user"
    pwd = "pwd"
    host = "127.0.0.1"
    port = 8000
    self.comms = pyrs.comms.SSHcomms(user,pwd,host,port);
    self.rpc = pyrs.rpc.RsRpc(self.comms); 

    # build responder (with Response Checker)
    self.responder = pyrs.responder.RsResponderGroup(self.rpc, self.parser);
    check_responder = pyrs.test.responders.RsCheckStatusResponder();
    self.responder.addGenericResponder(check_responder);

    self.reset()

  def reset(self):
    self._connected = False
    self.event_id_chat = None
    self._active_session = None
    self._active_session_ts = datetime.datetime.min

  def is_connected(self):
    return self._connected

  def connect_params(self, user, pwd, host, port):
    if self._connected:
      logging.info("pyrs.web.webharness.connect_params::already connected")
    else:
       self.comms.connect_params(user, pwd, host, port);
       self._connected = True

  def connect_state(self):
    if self._connected:
      return "Connected"
    return "not connected"

  def close(self):
    self.comms.close();
    self.reset()

  def active_session(self):
    if datetime.datetime.now() - self._active_session_ts > datetime.timedelta(minutes=5):
       logging.warning("Webharness.active_session() Reset")
       self._active_session = None

    logging.warning("Webharness.active_session() => %s, Age: %s" % 
        (self._active_session, datetime.datetime.now() - self._active_session_ts))
    return self._active_session

  def set_session(self, session_key):
    logging.warning("Webharness.set_session(%s)" % session_key)
    self._active_session = session_key
    self.keep_session_current()

  def keep_session_current(self):
    logging.warning("Webharness.keep_session_current()")
    self._active_session_ts = datetime.datetime.now()


  def send_request(self, msg_id, msg):
    try:
      req_id = self.rpc.request(msg_id, msg);
    except Exception, e:
      self._connected = False
      logging.info("webharness.send_request() Exception")
      raise e
    return req_id;

  def check_responses(self, timeout):

    now = datetime.datetime.now() - datetime.timedelta(seconds=1); # force one cycle at least.
    expiry_time = now + datetime.timedelta(seconds=timeout);
    while(now < expiry_time):
      print 'Doing handle responses cycle'
      more_resp = True;
      while(more_resp):
        # wait for responses.
        more_resp = self.responder.handleresponses()

      time.sleep(0.1);
      now = datetime.datetime.now();


  ######################################################################################
  ######################################################################################

  # get a specific response to a request.
  def specific_response(self, req_id):
    logging.info("webharness.response()")
    timeout = 2.0
    ans = self.rpc.response(req_id, timeout)
    if ans:
      (msg_id, msg_body) = ans;
      print "Received Response: msg_id: %d" % (msg_id);
      resp = self.parser.construct(msg_id, msg_body);
      if resp:
        print "Parsed Msg:";
        print resp;
        return (msg_id, resp)
    return None

  # get first. 
  def first_response(self):
    logging.info("webharness.first_response()")
    ans = self.rpc.first_response()
    if ans:
      (msg_id, msg_body) = ans;
      print "Received Response: msg_id: %d" % (msg_id);
      resp = self.parser.construct(msg_id, msg_body);
      if resp:
        print "Parsed Msg:";
        print resp;
        return (msg_id, resp)
    return None

  def get_event_chats(self):
    logging.info("webharness.get_event_chats()")
    if self.event_id_chat:
      return self.response(self.event_id_chat, 0)
    return None

  def get_event_id_chat(self):
    return self.event_id_chat

  ######################################################################################
  ######################################################################################

  # Specific requests for data....

  def request_peer_list(self, list_type):
    logging.info("webharness.request_peer_info()")

    # ignoring list_type for now.
    rp = peers_pb2.RequestPeers();

    if list_type == 'friends':
        rp.set = peers_pb2.RequestPeers.FRIENDS;
    elif list_type == 'connected':
        rp.set = peers_pb2.RequestPeers.CONNECTED;
    elif list_type == 'self':
        rp.set = peers_pb2.RequestPeers.OWNID;
    else:
        rp.set = peers_pb2.RequestPeers.ALL;

    #rp.set = peers_pb2.RequestPeers.VALID
    rp.info = peers_pb2.RequestPeers.ALLINFO;

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.PEERS, peers_pb2.MsgId_RequestPeers, False);

    req_id = self.send_request(msg_id, rp)
    return (req_id, msg_id)


  def request_peer_details(self, peer_id):
    logging.info("webharness.request_peer_details()")

    # ignoring list_type for now.
    rp = peers_pb2.RequestPeers();

    rp.set = peers_pb2.RequestPeers.LISTED;
    rp.info = peers_pb2.RequestPeers.ALLINFO;
    rp.pgp_ids.append(peer_id);

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.PEERS, peers_pb2.MsgId_RequestPeers, False);

    req_id = self.send_request(msg_id, rp)
    return (req_id, msg_id)


  def request_friend_add(self, peer_id, toadd):
    logging.info("webharness.request_friend_add()")

    # ignoring list_type for now.
    rp = peers_pb2.RequestAddPeer();

    if toadd:
      rp.cmd = peers_pb2.RequestAddPeer.ADD;
    else:
      rp.cmd = peers_pb2.RequestAddPeer.REMOVE;

    rp.pgp_id = peer_id;

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.PEERS, peers_pb2.MsgId_RequestAddPeer, False);

    req_id = self.send_request(msg_id, rp)
    return (req_id, msg_id)


  ######################################################################################
  ######################################################################################

  def request_system_status(self):
    logging.info("webharness.request_system_status()")

    rp = system_pb2.RequestSystemStatus();
    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.SYSTEM, system_pb2.MsgId_RequestSystemStatus, False);

    req_id = self.send_request(msg_id, rp)
    return (req_id, msg_id)






  ######################################################################################
  ######################################################################################


  def request_search_list(self, search_ids, limit):
    logging.info("webharness.request_search_list()")

    rp = search_pb2.RequestSearchResults()
    rp.result_limit = limit
    if search_ids is None:
      pass
    else:
      for id in search_ids:
        rp.search_ids.append(id)

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.SEARCH, search_pb2.MsgId_RequestSearchResults, False);
    req_id = self.send_request(msg_id, rp)
    return (req_id, msg_id)


  def request_close_search(self, search_id):
    logging.info("webharness.request_close_search()")

    rp = search_pb2.RequestCloseSearch()
    rp.search_id = search_id

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.SEARCH, search_pb2.MsgId_RequestCloseSearch, False);
    req_id = self.send_request(msg_id, rp)
    return (req_id, msg_id)



  def request_basic_search(self, search_terms):
    logging.info("webharness.request_basic_search()")

    rp = search_pb2.RequestBasicSearch();
    for term in search_terms:
      rp.terms.append(term)

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.SEARCH, search_pb2.MsgId_RequestBasicSearch, False);
    req_id = self.send_request(msg_id, rp)
    return (req_id, msg_id)



  ######################################################################################
  ######################################################################################



  def request_transfer_list(self, dir_upload):
    logging.info("webharness.request_transfer_list()")

    rp = files_pb2.RequestTransferList();
    if dir_upload:
      rp.direction = files_pb2.DIRECTION_UPLOAD
    else:
      rp.direction = files_pb2.DIRECTION_DOWNLOAD

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.FILES, files_pb2.MsgId_RequestTransferList, False);
    req_id = self.send_request(msg_id, rp)
    return (req_id, msg_id)


  def request_transfer_download(self, hash, filename, size):
    logging.info("webharness.request_transfer_download()")

    rp = files_pb2.RequestControlDownload()
    rp.file.hash = hash
    rp.file.name = filename
    rp.file.size = int(size)
    rp.action = files_pb2.RequestControlDownload.ACTION_START

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.FILES, files_pb2.MsgId_RequestControlDownload, False);
    req_id = self.send_request(msg_id, rp)
    return (req_id, msg_id)


  def request_dirlisting(self, peer_id, path):
    logging.info("webharness.request_dirlisting()")

    rp = files_pb2.RequestShareDirList()
    rp.ssl_id = peer_id;
    rp.path = path;

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.FILES, files_pb2.MsgId_RequestShareDirList, False);
    req_id = self.send_request(msg_id, rp)
    return (req_id, msg_id)


  ######################################################################################
  ######################################################################################

  def request_chat_lobby_list(self, list_type):
    logging.info("webharness.request_chat_lobby_list()")

    rp = chat_pb2.RequestChatLobbies();
    rp.lobby_set = chat_pb2.RequestChatLobbies.LOBBYSET_ALL;

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.CHAT, chat_pb2.MsgId_RequestChatLobbies, False);
    req_id = self.send_request(msg_id, rp)
    return (req_id, msg_id)


  def request_register_chat_lobby(self, list_type):
    logging.info("webharness.request_register_chat_lobby()")

    rp = chat_pb2.RequestChatLobbies();
    rp.lobby_set = chat_pb2.RequestChatLobbies.LOBBYSET_ALL;

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.CHAT, chat_pb2.MsgId_RequestRegisterEvents, False);
    req_id = rs.send_request(msg_id, rp)

    # slightly different... remember this parameter,
    self.event_id_chat = req_id
    return (req_id, msg_id)

  def request_set_chat_nickname(self, nickname):
    logging.info("webharness.request_set_chat_nickname()")

    rp = chat_pb2.RequestSetLobbyNickname();
    rp.nickname = nickname

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.CHAT, chat_pb2.MsgId_RequestSetLobbyNickname, False);
    req_id = self.request(msg_id, rp)
    return (req_id, msg_id)


  def request_join_or_leave_lobby(self, lobby_id, to_join):
    logging.info("webharness.request_join_or_leave_lobby()")
  
    rp = chat_pb2.RequestJoinOrLeaveLobby()
    rp.lobby_id = lobby_id
    if to_join:
      rp.action = chat_pb2.RequestJoinOrLeaveLobby.JOIN_OR_ACCEPT
    else:
      rp.action = chat_pb2.RequestJoinOrLeaveLobby.LEAVE_OR_DENY

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.CHAT, chat_pb2.MsgId_RequestJoinOrLeaveLobby, False);
    req_id = self.send_request(msg_id, rp)
    return (req_id, msg_id)


  def request_send_message(self, chat_type, chat_id, msg):
    logging.info("webharness.request_send_message()")

    rp = chat_pb2.RequestSendMessage();

    if chat_type == 'lobby':
        rp.msg.id.chat_type = chat_pb2.TYPE_LOBBY
    else:
        rp.msg.id.chat_type = chat_pb2.TYPE_PRIVATE

    rp.msg.id.chat_id = chat_id;
    rp.msg.msg = msg;

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.CHAT, chat_pb2.MsgId_RequestSendMessage, False);
    req_id = self.send_request(msg_id, rp)
    return (req_id, msg_id)


  def request_chat_history(self, chat_type, chat_id):
    logging.info("webharness.request_chat_history()")

    rp = chat_pb2.RequestChatHistory();

    if chat_type == 'lobby':
        rp.id.chat_type = chat_pb2.TYPE_LOBBY
    else:
        rp.id.chat_type = chat_pb2.TYPE_PRIVATE

    rp.id.chat_id = chat_id;

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.CHAT, chat_pb2.MsgId_RequestChatHistory, False);
    req_id = self.send_request(msg_id, rp)
    return (req_id, msg_id)



