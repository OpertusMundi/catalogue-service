
import uuid
import logging
import json
import pkgutil
from datetime import datetime
from jsonschema import validate
from catalogueapi.database import db
from catalogueapi.database.model.item import Item, Draft, History

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


def update_item(item, data):

    data['properties']['metadata_date'] = datetime.now()
    item.update(item.id, data)
    session.add(item)
    session.commit()

    log.info('Updated item %s', item.id)


def delete_item(id):
    item = session.query(Item).get(id)
    data = item.item_geojson
    # keep a record in history table
    data['properties']['deleted_at'] = datetime.now()
    data['properties']['deleted'] = True
    history = History()
    history.update(id, data)
    session.add(history)
    session.delete(item)
    session.commit()
    
    log.info('Deleted item %s', id)


def create_draft(data):
    if not 'id' in data or not is_valid_uuid(data['id']):
        id = str(uuid.uuid4())
    else:
        id = data['id']
    draft = Draft()
    data['properties']['status'] = 'draft'
    if not data['properties'].get('version'):
        data['properties']['version'] = '1.0'
    data['properties']['created_at'] = datetime.now()
    draft.update(id, data)
    session.add(draft)
    session.commit()
    log.info('Created draft %s', id)
    return id


def create_draft_from_item(item):
    data = item.item_geojson
    data['properties']['status'] = 'draft'
    draft = Draft()
    draft.update(item.id, data)
    session.add(draft)
    session.commit()
    log.info('Created draft from item %s', id)
    return id


def update_draft(draft, data):

    data['properties']['metadata_date'] = datetime.now()
    draft.update(draft.id, data)
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
            # keep a record in history table
            old_data = item.item_geojson
            old_data['properties']['deleted'] = False
            history = History()
            history.update(id, old_data)
            session.add(history)
            # increment version number
            version = data['properties'].get('version')
            version = version.split('.')
            version[-1] = str(int(version[-1]) + 1)
            data['properties']['version'] = '.'.join(version)
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

    return 


def validate_input(data):

    schema = pkgutil.get_data('catalogueapi', "resources/record.json")
    validate(instance=data, schema=json.loads(schema))