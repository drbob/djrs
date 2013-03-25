"""
Djrs cxfreeze script.
"""
import sys

# explicit imports to fix brokenness.
import encodings.hex_codec

# fix path for local packages.
import djrs_path

base=None

# Build on Linux or Windows.
if sys.platform in ['linux2', 'win32']:
  from cx_Freeze import setup, Executable
  copyDependentFiles = True

  includes = [
    #'Crypto',
    #'encodings',
    'django.template.loader_tags',
    #'libs.rs_logging',
  ]

  include_files = [
    'templates/base.dtml',
    'templates/base_loggedout.dtml',
    'templates/base_sidebar.dtml',
    'templates/djrs_about.dtml',
    'templates/djrs_apps.dtml',
    'templates/djrs_busy.dtml',
    'templates/djrs_chat.dtml',
    'templates/djrs_chat_friend.dtml',
    'templates/djrs_chat_lobby.dtml',
    'templates/djrs_error.dtml',
    'templates/djrs_friends.dtml',
    'templates/djrs_friend_details.dtml',
    'templates/djrs_home.dtml',
    'templates/djrs_login.dtml',
    'templates/djrs_search.dtml',
    'templates/djrs_transfers.dtml',
    'static/js/bootstrap.min.js',
    'static/js/jquery-1.8.1.js',
    'static/css/bootstrap-responsive.min.css',
    'static/css/bootstrap.min.css',
    'static/img/glyphicons-halflings.png',
    'static/img/glyphicons-halflings-white.png',
  ]

  build_exe_options = {"packages": ["os"],
                       "includes": includes,
                       "include_files": include_files,
                       }
  setup(name = "djrs",
        version = "0.1",
        description = "djrs: Retroshare Web Interface.",
        options = {"build_exe": build_exe_options},
        executables = [Executable("djrs_server.py", base=base)])

