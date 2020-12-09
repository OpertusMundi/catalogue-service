import logging
import json
import requests

import catalogueapi.database.actions.item as actions
from catalogueapi.database.model.item import Item

log = logging.getLogger(__name__)


def harvest(url, harvester='op-catalogue'):
    result = requests.get(url).json()
    if harvester == 'op-catalogue':
        items = result.get('result').get('items')
        harvested = _from_op_catalogue(items, url)
    elif harvester == 'ckan':
        items = result.get('result').get('results')
        harvested = _from_ckan(items, url)
    items = Item.query
    harvested_ids = []
    for harvest in harvested:
        id = harvest.get('id')
        item = items.filter(Item.id == id).first()
        if not item:
            log.info('Harvesting item %s', id)
            actions.create_item(harvest)
        # update if version is changed
        elif harvest['properties']['metadata_version'] and item.metadata_version != harvest['properties']['metadata_version']:
            actions.update_item(item, harvest)
        harvested_ids.append(id)
    # update any existing harvested data deleted in remote
    items = items.filter(Item.harvested_from == url)
    for item in (item for item in items if item.id not in harvested_ids):
        actions.delete_item(item.id)


def _from_ckan(harvested, url):
    result = []
    for h in harvested:
        item = {}
        item['properties'] = {}
        item['id'] = h.get('id')
        item['properties']['title'] = h.get('title')
        item['properties']['abstract'] = h.get('notes')
        item['properties']['license'] = h.get('license_title')
        item['properties']['keywords'] = []
        for tag in h.get('tags'):
            item['properties']['keywords'].append(tag.get('name'))
        item['properties']['metadata_version'] = h.get('version')
        item['properties']['metadata_date'] = h.get('metadata_modified')
        item['properties']['additional_resources'] = []
        for resource in h.get('resources'):
            item['properties']['additional_resources'].append(
                resource.get('url'))

        datacite = h.get('datacite')
        if datacite:
            item['properties']['metadata_point_of_contact_email'] = datacite.get(
                'contact_email')
            item['properties']['topic_categories'] = []
            for s in h.get('closed_tag'):
                item['properties']['topic_categories'].append(s)
            item['properties']['additional_resources'].append(
                datacite.get('related_publication'))
            item['properties']['language'] = datacite.get('languagecode')
        inspire = h.get('inspire')
        if inspire:
            bbox = inspire.get('bounding_box')
            if bbox:
                item['geometry'] = {'type': 'Polygon'}
                item['geometry']['coordinates'] = [[[bbox[0]['sblat'], bbox[0]['wblng']],
                                                    [bbox[0]['sblat'], bbox[0]['eblng']],
                                                    [bbox[0]['nblat'], bbox[0]['eblng']],
                                                    [bbox[0]['nblat'], bbox[0]['wblng']],
                                                    [bbox[0]['sblat'], bbox[0]['wblng']]]]
        item['properties']['harvested_from']= url
        item['properties']['harvest_json']= json.dumps(h)
        result.append(item)
    return result


def _from_op_catalogue(harvested):
    result= []
    for h in harvested:
        item= {}
        item['properties']= h.get('properties')
        item['properties']['harvested_from']= url
        item['properties']['harvest_json']= json.dumps(h)
        result.append(item)
    return result
