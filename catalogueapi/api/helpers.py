import logging

log = logging.getLogger(__name__)

def convert_from_iso(md):
    item = {}
    item['id'] = md.identifier
    item['type'] = 'Feature'
    item['properties'] = {}
    item['properties']['title']= md.identification.title
    item['properties']['abstract']= md.identification.abstract
    item['properties']['keywords'] = []
    for k in md.identification.keywords2:
        for key in k.keywords:
            theme = ''
            if k.thesaurus:
                theme = k.thesaurus['title']
            item['properties']['keywords'].append({'keyword': key , 'theme': theme })

    for t in md.identification.topiccategory:
        item['properties']['keywords'].append({'keyword': t , 'theme': '' })
    if md.identification.uselimitation:
        item['properties']['license']= md.identification.uselimitation[0]
    date_start = md.identification.temporalextent_start
    date_end = md.identification.temporalextent_end
    if date_start:
        item['properties']['date_start'] = date_start
    if date_end:
        item['properties']['date_end'] = date_end

    bbox = md.identification.bbox
    if bbox:
        item['geometry'] = {'type': 'Polygon'}
        item['geometry']['coordinates'] = [[[float(bbox.minx), float(bbox.miny)],
                                                [float(bbox.minx), float(bbox.maxy)],
                                                [float(bbox.maxx), float(bbox.maxy)],
                                                [float(bbox.maxx), float(bbox.miny)],
                                                [float(bbox.minx), float(bbox.miny)]]]
    if md.contact:
        if md.contact[0].email:
            item['properties']['metadata_point_of_contact_email'] = md.contact[0].email
        if md.contact[0].name:
            item['properties']['metadata_point_of_contact_name'] = md.contact[0].name
    l = md.languagecode
    if l == 'eng': l = 'en'
    elif l == 'gre': l = 'el'
    item['properties']['language']= l
    item['properties']['reference_system']= md.referencesystem.code
    item['properties']['lineage'] = md.dataquality.lineage


    return item