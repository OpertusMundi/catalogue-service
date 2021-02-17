import logging
import json
import requests
from owslib.iso import *
from owslib.csw import CatalogueServiceWeb

import catalogueapi.database.actions.item as actions
from catalogueapi.database.model.item import Item

log = logging.getLogger(__name__)


def harvest(url, harvester='csw'):
    result = requests.get(url)
    if harvester == 'opertusmundi':
        items = result.json().get('result').get('items')
        harvested = _from_op_catalogue(items, url)
    elif harvester == 'ckan':
        items = result.json().get('result').get('results')
        harvested = _from_ckan(items, url)
    elif harvester == 'csw':
        harvested = _from_csw(url)
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
    
    return len(harvested)


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


def _from_op_catalogue(harvested, url):
    result= []
    for h in harvested:
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
            item = {}
            item['id'] = value.identifier
            item['properties'] = {}
            item['properties']['title']= value.identification.title
            item['properties']['abstract']= value.identification.abstract
            item['properties']['keywords'] = []
            for k in value.identification.keywords2:
                for key in k.keywords:
                    theme = ''
                    if k.thesaurus:
                        theme = k.thesaurus['title']
                    item['properties']['keywords'].append({'keyword': key , 'theme': theme })

            for t in value.identification.topiccategory:
                item['properties']['keywords'].append({'keyword': t , 'theme': '' })
            item['properties']['license']= value.identification.uselimitation
            item['properties']['date_start'] = value.identification.temporalextent_start
            item['properties']['date_end'] = value.identification.temporalextent_end

            bbox = value.identification.bbox
            if bbox:
                item['geometry'] = {'type': 'Polygon'}
                item['geometry']['coordinates'] = [[[float(bbox.minx), float(bbox.miny)],
                                                        [float(bbox.minx), float(bbox.maxy)],
                                                        [float(bbox.maxx), float(bbox.maxy)],
                                                        [float(bbox.maxx), float(bbox.miny)],
                                                        [float(bbox.minx), float(bbox.miny)]]]
            if value.contact:
                item['properties']['metadata_point_of_contact_email'] = value.contact[0].email
                item['properties']['metadata_point_of_contact_name'] = value.contact[0].name
            l = value.languagecode
            if l == 'eng': l = 'en'
            elif l == 'gre': l = 'el'
            item['properties']['language']= l
            item['properties']['reference_system']= value.referencesystem.code
            item['properties']['lineage'] = value.dataquality.lineage

            item['properties']['harvested_from']= url
            item['properties']['harvest_json']= value.xml.decode()

        result.append(item)

        flag = 1

    return result