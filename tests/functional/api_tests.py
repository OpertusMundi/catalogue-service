import logging
import json
import os

app = None

#
# Setup/Teardown module
#

def setup_module():
    global app
    from . import app as _app
    app = _app
    print(" === Setting up tests for module %s with %s"  % (__name__, app))
    pass

def teardown_module():
    global app
    app = None
    print(" === Tearing down tests for module %s"  % (__name__))
    pass

#
# Tests
#

def test_get_documentation_1():
    with app.test_client() as client:
        res = client.get('/api/swagger.json', query_string=dict(), headers=dict())
        assert res.status_code == 200
        r = res.get_json();
        assert not (r.get('swagger') is None)

