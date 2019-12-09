
import uuid
import logging

from catalogueapi.database import db
from catalogueapi.database.model.item import Item 

log = logging.getLogger(__name__)
session = db.session

def create_item(data):
    if not 'item_id' in data or not is_valid_uuid(data['item_id']):
        data['item_id'] = str(uuid.uuid4())
    item = Item(data)
    session.add(item)
    session.commit()
    log.info('Created item %s', data['item_id'])

def update_item(item_id, data):

    item = session.query(Item).get(item_id)
    data['item_id'] = item_id
    item.title = data.get('title')
    item.description = data.get('description')
    item.creator = data.get('creator')
    session.add(item)
    session.commit()
    log.info('Updated item %s', item_id)

def delete_item(item_id):

    item = session.query(Item).get(item_id)
    session.delete(item)
    session.commit()
    log.info('Deleted item %s', item_id)

def is_valid_uuid(uuid_to_test, version=4):
    try:
        s = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return s