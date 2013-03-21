"""
Djrs cxfreeze script.
"""
import sys

# explicit imports to fix brokenness.
import encodings.hex_codec

# Build on Linux or Windows.
if sys.platform in ['linux2', 'win32']:
  from cx_Freeze import setup, Executable
  copyDependentFiles = True

  includes = [
    #'Crypto',
    #'encodings',
    'django.template.loader_tags',
  ]

  build_exe_options = {"packages": ["os"],
                       "includes": includes
                       }
  setup(name = "djrs",
        version = "0.1",
        description = "djrs: Retroshare Web Interface.",
        options = {"build_exe": build_exe_options},
        executables = [Executable("djrs_exec.py", base=base)])

