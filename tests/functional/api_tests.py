import logging
import json
import os

app = None

resources_dir = None

#
# Setup/Teardown module
#

def setup_module():
    global app
    global resources_dir
    from . import app as _app, resources_dir as _resources_dir
    app = _app
    resources_dir = _resources_dir
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

def test_draft_search_1():
    with app.test_client() as client:
        res = client.get('/api/draft/search', query_string=dict())
        print("test_draft_search_1: res=%r" % (res))
        assert res.status_code in [200, 404]

def test_draft_create_1():
    with app.test_client() as client:
        req_data = None
        with open(os.path.join(resources_dir, 'draft-1.json')) as f: 
            req_data = json.load(f)
        res = client.post('/api/draft/create', json=req_data)
        assert res.status_code == 200
    
