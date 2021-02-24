import logging
import json
import requests
from owslib.iso import *
from owslib.csw import CatalogueServiceWeb

import catalogueapi.database.actions.item as actions
from catalogueapi.database.model.item import Harvest
from catalogueapi.api.helpers import convert_from_iso

log = logging.getLogger(__name__)


def harvest(url, harvester='csw'):
    result = requests.get(url)
    if harvester == 'opertusmundi':
        items = result.json().get('result').get('items')
        new_items = _from_op_catalogue(items, url)
    elif harvester == 'ckan':
        items = result.json().get('result').get('results')
        new_items = _from_ckan(items, url)
    elif harvester == 'csw':
        new_items = _from_csw(url)

    harvests = Harvest.query
    harvested_ids = []

    for data in new_items:
        id = data.get('id')
        harvest = harvests.filter(Harvest.id == id).first()
        if not harvest:
            log.info('Harvesting item %s', id)
            actions.create_harvested_item(data)
        # update if it exists
        else:
            actions.update_harvested_item(harvest, data)
        harvested_ids.append(id)
    # delete any existing harvested data deleted in remote
    harvests = harvests.filter(Harvest.harvested_from == url)
    for harvest in (h for h in harvests if h.id not in harvested_ids):
        log.debug('Deleting harvest %s', harvest.id)
        actions.delete_harvested_item(harvest.id)
    
    return len(new_items)


def _from_ckan(new_items, url):
    result = []
    for h in new_items:
        item = {}
        item['properties'] = {}
        item['id'] = h.get('id')
        item['properties']['title'] = h.get('title')
        item['properties']['abstract'] = h.get('notes')
        item['properties']['license'] = h.get('license_title')
        item['properties']['keywords'] = []
        if 'tags' in h:
            for tag in h.get('tags'):
                item['properties']['keywords'].append({'keyword': tag.get('name') , 'theme': '' })
        item['properties']['metadata_version'] = h.get('version')
        item['properties']['metadata_date'] = h.get('metadata_modified')
        item['properties']['resources'] = []
        for resource in h.get('resources'):
            item['properties']['resources'].append({
                'id': resource.get('id'),
                'category': '',
                'value': resource.get('url'),
                'format': resource.get('format')})

        datacite = h.get('datacite')
        if datacite:
            item['properties']['metadata_point_of_contact_email'] = datacite.get(
                'contact_email')
            item['properties']['topic_categories'] = []
            for s in h.get('closed_tag'):
                item['properties']['keywords'].append({'keyword': s , 'theme': '' })
            item['properties']['additional_resources'] = []
            item['properties']['additional_resources'].append(({
                'id': resource.get('id'),
                'type': '',
                'value': datacite.get('related_publication'),
                'name': 'related_publication'})
                )
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
        if len(result) == 21: break
    return result


def _from_op_catalogue(new_items, url):
    result= []
    for h in new_items:
        h['properties']['harvested_from']= url
        h['properties']['harvest_json']= json.dumps(h)
        result.append(h)
    return result

def _from_csw(url):
    result=[]

    schema = 'http://www.isotc211.org/2005/gmd'

    src = CatalogueServiceWeb(url)
    
    stop = 0
    flag = 0
    maxrecords = 5
    totalrecords = 20

    while stop == 0:
        if flag == 0:  # first run, start from 0
            startposition = 0
        else:  # subsequent run, startposition is now paged
            startposition = src.results['nextrecord']

        src.getrecords2(esn='full', startposition=startposition, maxrecords=maxrecords, outputschema=schema)

        if src.results['nextrecord'] == 0 \
            or src.results['returned'] == 0 \
            or src.results['nextrecord'] > src.results['matches'] \
            or len(result) >= totalrecords:  # end the loop, exhausted all records
            stop = 1
            break
        

        # harvest each record
        for key, value in src.records.items():
            item = convert_from_iso(value)

            item['properties']['harvested_from']= url
            item['properties']['harvest_json']= value.xml.decode()

        result.append(item)

        flag = 1

    return result