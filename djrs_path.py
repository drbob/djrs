
import os, sys

# This seems to be only needed by Windows.
if sys.platform in ['win32']:
    # setup path.

    # windows doesn't like __file__ 
    # this is a problem, as we will have to run from 
    # from the build directory - otherwise this will be wrong.
    # but we will deal with this later!
    app_dir = os.path.abspath(os.getcwd())
    sys.path.append(os.path.join(app_dir, 'submodules', 'pyrs'))
    sys.path.append(os.path.join(app_dir, 'libs'))

    # everyone needs to app_dir
    sys.path.append(os.path.dirname(app_dir))

    print sys.path

else: 
    app_dir = os.path.abspath(os.path.dirname(__file__))

