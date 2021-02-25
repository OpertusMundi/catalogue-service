import logging
import json
import os

from catalogueapi.app import create_app

# Setup/Teardown

app = None

def setup_package():
    print(" == Setting up functional tests")
    
    os.environ['TESTING'] = 'True'
    os.environ['FLASK_ENV'] = 'testing'
    
    global app
    if 'FILE_CONFIG' in os.environ:
        app = create_app(os.path.realpath(os.environ['FILE_CONFIG']))
    else:
        app = create_app()

def teardown_package():
    print(" == Tearing down functional tests")
    pass

