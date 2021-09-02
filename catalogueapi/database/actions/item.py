import uuid
import logging
import json
import jsonschema
import os
from datetime import datetime
import catalogueapi.resources
from catalogueapi.database import db
from catalogueapi.database.model.item import Item, Draft, History, Harvest

log = logging.getLogger(__name__)

# Initialize JSON-Schema validator

_schema = None
_resources_dir = catalogueapi.resources.base_dir()
with open(os.path.join(_resources_dir, 'record.json')) as f:
    _schema = json.load(f)

_validator = jsonschema.Draft7Validator(_schema, 
    resolver=jsonschema.RefResolver('file://' + _resources_dir, _schema));

def validate_input(data):
    return _validator.validate(data)

# Actions

session = db.session

def create_item(data):
    item = Item()
    if not data['properties'].get('metadata_version'):
        data['properties']['metadata_version'] = '1.0'
    data['properties']['created_at'] = datetime.now()
    id = data['id']
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
    draft = Draft()
    data['properties']['status'] = 'draft'
    if not data['properties'].get('version'):
        data['properties']['version'] = '1.0'
    data['properties']['metadata_version'] = '1.0'
    data['properties']['created_at'] = datetime.now()
    id = data['id']
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


def create_harvested_item(data):
    id = data['id']
    harvest = Harvest()
    if not data['properties'].get('metadata_version'):
        data['properties']['metadata_version'] = '1.0'
    data['properties']['created_at'] = datetime.now()
    harvest.update(id, data)
    session.add(harvest)
    session.commit()
    log.info('Created harvested item %s', id)
    return harvest


def update_harvested_item(harvest, data):

    data['properties']['metadata_date'] = datetime.now()
    harvest.update(harvest.id, data)
    session.add(harvest)
    session.commit()

    log.info('Updated harvested item %s', id)


def delete_harvested_item(id):

    harvest = session.query(Harvest).get(id)
    session.delete(harvest)
    session.commit()
    log.info('Deleted harvest %s', id)



def update_status(id, status):
    draft = Draft.query.filter(Draft.id == id).one()
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
            # increment metadata version number
            metadata_version = data['properties'].get('metadata_version')
            metadata_version = metadata_version.split('.')
            metadata_version[-1] = str(int(metadata_version[-1]) + 1)
            data['properties']['metadata_version'] = '.'.join(metadata_version)
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


