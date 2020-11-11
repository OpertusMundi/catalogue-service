
import uuid
import logging
import json
from datetime import datetime

from catalogueapi.database import db
from catalogueapi.database.model.item import Item, Draft 

log = logging.getLogger(__name__)
session = db.session

def create_item(data):
    if not 'id' in data or not is_valid_uuid(data['id']):
        id = str(uuid.uuid4())
    else:
        id = data['id']
    item = Item()
    item.update(id, data)
    session.add(item)
    session.commit()
    log.info('Created item %s', id)
    return item

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

def create_draft(data):
    if not 'id' in data or not is_valid_uuid(data['id']):
        id = str(uuid.uuid4())
    draft = Draft()
    data['properties']['status'] = 'draft'
    data['properties']['created_at'] = datetime.now()
    draft.update(id, data)
    session.add(draft)
    session.commit()
    log.info('Created draft %s', id)
    return id

def create_draft_from_item(id):
    item = session.query(Item).get(id)
    data = item.item_geojson
    draft = Draft()
    draft.update(id, data)
    draft.status = 'draft'
    session.add(draft)
    session.commit()
    log.info('Created draft from item %s', id)
    return id

def update_draft(id, data):
    
    draft = session.query(Draft).get(id)
    data['properties']['modified_at'] = datetime.now()
    draft.update(id, data)
    session.add(draft)
    session.commit()
    
    log.info('Updated draft %s', id)

def delete_draft(id):

    draft = session.query(Draft).get(id)
    session.delete(draft)
    session.commit()
    log.info('Deleted draft %s', id)

def update_status(id, status):
    draft = session.query(Draft).get(id)
    data = draft.item_geojson
    if status == 'published':
        data['properties']['publication_date'] = datetime.now()
        item = session.query(Item).get(id)
        if item:
            item.update(id, data)
        else:
            item = create_item(data)
        session.add(item)
        session.delete(draft)
    else:
        if status == 'accepted':
            data['properties']['accepted_at'] = datetime.now()
        elif status == 'review':
            data['properties']['submitted_at'] = datetime.now()
        data['properties']['status'] = status
        draft.update(id, data)
        session.add(draft)
    session.commit()
    log.info('Updated item %s with status %s', id, status)

def is_valid_uuid(uuid_to_test, version=4):
    try:
        s = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return s
