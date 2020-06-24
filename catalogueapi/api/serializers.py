from flask_restx import fields
from catalogueapi.api.restx import api

polygon = api.model('Polygon geometry', {
    'type': fields.String(description='Type of geometry', default="Polygon"),
    'coordinates': fields.List(fields.List(
        fields.List(fields.Float, type="Array"),
        required=True,
        default=[[13.4197998046875, 52.52624809700062],
                 [13.387527465820312, 52.53084314728766],
                 [13.366928100585938, 52.50535544522142],
                 [13.419113159179688, 52.501175722709434],
                 [13.4197998046875, 52.52624809700062]]
    )
    )
})

properties = api.model('Properties of an item', {
    'title': fields.String(description='A name given to the resource'),
    'abstract': fields.String(description='An abstract of the resource'),
    'type': fields.String(description='The nature or genre of the resource'),
    'spatial_data_service_type': fields.String(description='The nature or genre of the service'),
    'format': fields.String(description='The file format, physical medium, or dimensions of the resource'),
    'keywords': fields.List(fields.String(description='The topic of the resource')),
    'publisher_name': fields.String(description='Name of an entity responsible for making the resource available'),
    'publisher_email': fields.String(description='Email of an entity responsible for making the resource available'),
    'language': fields.String(description='A language of the resource'),
    'date_start': fields.Date(description='The temporal extent of the resource (start date)'),
    'date_end': fields.Date(description='The temporal extent of the resource (end date))'),
    'creation_date': fields.Date(description='A point or period of time associated with the creation event \
                    in the lifecycle of the resource'),
    'publication_date': fields.Date(description='A point or period of time associated with the publication event \
                    in the lifecycle of the resource'),
    'revision_date': fields.Date(description='A point or period of time associated with the revision event  \
                    in the lifecycle of the resource '),
    'resource_locator': fields.String(description='The ‘navigation section’ of a metadata record which point users to the location (URL) \
                    where the data can be downloaded, or to where additional information about the resource may be provided'),
    'license': fields.String(description='Information about resource licensing'),
    'topic_category': fields.String(description='A high-level classification scheme to assist in the grouping and topic-based \
                    search of available spatial data resources'),
    'reference_system': fields.String(description='Information about the reference system'),
    'spatial_resolution': fields.String(description='Spatial resolution refers to the level of detail of the data set'),
    'scale': fields.String(description='Denominator of the scale of the data set'),
    'version': fields.String(description='Version of the resource'),
    'conformity': fields.String(description='Degree of conformity with the implementing rules/standard of the metadata followed'),
    'additional_resources': fields.String(description='Auxiliary files or additional resources to the dataset.'),
    'public_access_limitations': fields.String(description='Information on the limitations and the reasons for them'),

    'metadata_language': fields.String(description='The language in which the metadata elements are expressed'),
    'metadata_point_of_contact_name': fields.String(description='The name of the organisation responsible for the creation \
                     and maintenance of the metadata'),
    'metadata_point_of_contact_email': fields.String(description='The email of the organisation responsible for the creation \
                     and maintenance of the metadata'),
    'metadata_date': fields.Date(description='The date which specifies when the metadata record was created or updated'),
    'coupled_resource': fields.String(description='Provides information about the datasets that the service operates on'),
    'lineage': fields.String(description='General explanation of the data producer’s knowledge about the lineage of a dataset'),
    'parent_id': fields.String(description='Provides the ID of a parent dataset.')
})

item_geojson = api.model('The item in geojson format',{
    'id': fields.String(readOnly=True, description='An unambiguous reference to the resource within a given context'),
    'type': fields.String(description='The type of the geojson', default='Feature'),
    'geometry': fields.Nested(polygon, description='The spatial extent of the resource, the spatial \
                    applicability of the resource, or the jurisdiction under which the resource is relevant.'),
    'properties':fields.Nested(properties, description='The properties of the geojson.')
})

page_of_items = api.model('A page of results', {
    'items': fields.List(fields.Nested(item_geojson)),
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})



