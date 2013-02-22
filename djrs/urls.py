from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'djrs.views.home', name='djrs_home'),
    url(r'^login/$', 'djrs.views.login', name='djrs_login'),
    url(r'^busy/$', 'djrs.views.busy', name='djrs_busy'),
    url(r'^friends/$', 'djrs.views.friends', name='djrs_friends'),
    url(r'^friends/(?P<list_type>\w+)/$', 'djrs.views.friends', name='djrs_friends'),
    url(r'^friend/(?P<friend_id>\w+)/$', 'djrs.views.friend_details', name='djrs_friend_details'),

    url(r'^apps/$', 'djrs.views.apps', name='djrs_apps'),
    url(r'^about/$', 'djrs.views.about', name='djrs_about'),

    url(r'^chat/$', 'djrs.views.chat', name='djrs_chat'),
    url(r'^chat/friend/(?P<peer_id>\w+)/$', 'djrs.views.chat_friend', name='djrs_chat_friend'),
    url(r'^chat/lobby/(?P<lobby_id>\w+)/$', 'djrs.views.chat_lobby', name='djrs_chat_lobby'),

    url(r'^lobby/(?P<lobby_id>\w+)/join/$', 'djrs.views.lobby_join', name='djrs_lobby_join'),
    url(r'^lobby/(?P<lobby_id>\w+)/drop/$', 'djrs.views.lobby_drop', name='djrs_lobby_drop'),
    url(r'^lobby/(?P<lobby_id>\w+)/$', 'djrs.views.chat_lobby', name='djrs_chat_lobby2'),
    url(r'^message/(?P<chat_type>\w+)/(?P<chat_id>\w+)$', 'djrs.views.chat_send', name='djrs_chat_send'),

    url(r'^transfers/$', 'djrs.views.transfers', name='djrs_transfers'),
    url(r'^transfer/(?P<hash>\w+)/download/$', 'djrs.views.transfer_download', name='djrs_transfer_download'),
    url(r'^transfer/(?P<hash>\w+)/pause/$', 'djrs.views.transfer_pause', name='djrs_transfer_pause'),
    url(r'^transfer/(?P<hash>\w+)/cancel/$', 'djrs.views.transfer_cancel', name='djrs_transfer_cancel'),

    url(r'^searches/$', 'djrs.views.searches', name='djrs_searches'),
    url(r'^search/(?P<search_id>\d+)/$', 'djrs.views.search_details', name='djrs_search_details'),
    url(r'^search/(?P<search_id>\d+)/close/$', 'djrs.views.search_close', name='djrs_search_close'),
)
