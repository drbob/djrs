
# Dependencies.
# cx_freeze cannot discover django's dependencies, 
# as it does a lot of automagic importing.
#
# So we have explicit imports to fix brokenness,  

# At system level.
import encodings.hex_codec
import encodings.ascii
import encodings.latin_1
import encodings.utf_8

# At Django Level
# DB
import django.db.backends.sqlite3
import django.db.backends.sqlite3.base
import sqlite3

# Middleware
import django.middleware.common
import django.contrib.sessions.middleware
import django.middleware.csrf
import django.contrib.auth.middleware
import django.contrib.messages.middleware

# Session / Cache
import django.contrib.sessions.backends.cache
import django.core.cache.backends.locmem

# Messages.
import django.contrib.messages.storage.fallback

# Templates.
import django.template.base
import django.template.defaulttags
import django.template.defaultfilters
import django.template.loader
import django.template.loaders.filesystem
import django.template.loaders.app_directories

# This one cannot be imported directly, 
# it must be included via cx_freeze configuration file.
#import django.template.loader_tags

# Context Processors
import django.contrib.auth.context_processors
import django.core.context_processors
import django.contrib.messages.context_processors

# Django Apps.
import django.contrib.auth
import django.contrib.contenttypes
import django.contrib.sessions
import django.contrib.sites
import django.contrib.messages
import django.contrib.staticfiles


# At App Level.

# dependencies
import paramiko
import google.protobuf.descriptor

# Apps.
import djrs.urls
import djrs.middleware
import djrs.context_processors
import djrs.views
import djrs.forms


