
import uuid
import logging
import json

from catalogueapi.database import db
from catalogueapi.database.model.item import Item 

log = logging.getLogger(__name__)
session = db.session

def create_item(data):
    if not 'id' in data or not is_valid_uuid(data['id']):
        id = str(uuid.uuid4())
    item = Item()
    item.update(id, data)
    session.add(item)
    session.commit()
    log.info('Created item %s', id)

def update_item(id, data):
    
    item = session.query(Item).get(id)
    item.update(id, data)
    session.add(item)
    session.commit()
    
    log.info('Updated item %s', id)

def delete_item(id):

    item = session.query(Item).get(id)
    session.delete(item)
    session.commit()
    log.info('Deleted item %s', id)

def is_valid_uuid(uuid_to_test, version=4):
    try:
        s = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return s
