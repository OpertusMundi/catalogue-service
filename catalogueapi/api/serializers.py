from flask_restx import fields, inputs
from catalogueapi.api.restx import api

polygon = api.model('polygon geometry', {
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

keyword = api.model('keyword', {
        'keyword': fields.String(description='keyword value'),
        'theme': fields.String(description='a related theme')
} )

scale = api.model('scale', {
        'scale': fields.Integer(description='scale value'),
        'description': fields.String(description='a short description')
} )

additional_resources = api.model('additional_resources', {
        'id': fields.String(),
        'type': fields.String(),
        'value': fields.String(),
        'name': fields.String(),
        'size': fields.Integer(),
        'modified_on': fields.DateTime()
} )

attributes = api.model('attributes', {
        'queryable': fields.Boolean(),
        'cascaded': fields.Boolean(),
        'opaque': fields.Boolean(),
        'no_subsets': fields.Boolean(),
        'fixed_width': fields.Integer(),
        'fixed_height': fields.Integer(),
})

dimension = api.model('dimension', {
        'name': fields.String(),
        'unit': fields.String(),
        'default': fields.String(),
        'values': fields.List(fields.String()),
})

resource = api.model('resource', {
        'id': fields.String(),
        'parent_id': fields.String(),
        'filename': fields.String(),
        'endpoint': fields.String(),
        'size': fields.Integer(),
        'type': fields.String(enum=['FILE', 'SERVICE', 'ASSET']),
        'category': fields.String(enum=['VECTOR', 'RASTER', 'NETCDF', 'TABULAR', 'BUNDLE', 'SERVICE']),
        'service_type': fields.String(enum=["TMS", "WMS", "WFS", "WCS", "CSW", "Data API", "OGC API"]),
        'format': fields.String(),
        'encoding': fields.String(),
        'modified_on': fields.DateTime(),
        'style': fields.List(fields.Raw()),
        'crs': fields.List(fields.String()),
        'bbox': fields.Raw(),
        'dimension':  fields.List(fields.Nested(dimension)),
        'output_formats': fields.List(fields.String()),
        'filter_capabilities': fields.List(fields.String()),
        'attribution': fields.String(),
        'min_scale': fields.Integer(),
        'max_scale': fields.Integer(),
        'attributes': fields.Nested(attributes)

} )

responsible_party = api.model('responsible_party', {
        'name': fields.String(description = 'Name of person responsible for making the resource available'),
        'organization_name': fields.String(description = 'Name of entity responsible for making the resource available'),
        'email': fields.String(description = 'Email of entity responsible for making the resource available'),
        'phone': fields.String(description = 'Email of entity responsible for making the resource available'),
        'address': fields.String(description = 'Address of entity responsible for making the resource available'),
        'service_hours': fields.String(description = 'Contact hours of entity responsible for making the resource available'),
        'role': fields.String(description='Role of entity responsible for making the resource available',
                enum=['publisher', 'owner', 'custodian', 'user', 'distributor', 'originator', 'point of contact', 'processor', 'author']),
} )

properties = api.model('properties of an item', {
    'title': fields.String(description='A name given to the resource', required=True),
    'abstract': fields.String(description='An abstract of the resource'),
    'type': fields.String(description='The nature or genre of the resource', enum = ["sentinel-hub-open-data", "raster", "vector", "service", "tabular", "bundle", "netcdf"]),
    'spatial_data_service_type': fields.String(description='The nature or genre of the service', enum=["TMS", "WMS", "WFS", "WCS", "CSW", "Data API", "OGC API"]),
    'spatial_data_service_version': fields.String(description='The version of the implemented service specification'),
    'spatial_data_service_operations': fields.List(fields.String(description='The operations supported by the service')),
    'spatial_data_service_queryables': fields.List(fields.String(description='The queryables supported by the service')),

    'format': fields.String(description='The file format, physical medium, or dimensions of the resource'),
    'keywords':  fields.List(fields.Nested(keyword,description='The topic of the resource')),
    'responsible_party':  fields.List(fields.Nested(responsible_party,description='The responsible party (including contact information) of the resource')),
    'publisher_name': fields.String(description='Name of an entity responsible for making the resource available'),
    'publisher_email': fields.String(description='Email of an entity responsible for making the resource available'),
    'publisher_id': fields.String(description='Id of an entity responsible for making the resource available'),
    'language': fields.String(description='A language of the resource'),
    'status': fields.String(readonly = True, description='The status of the item'),

    'date_start': fields.DateTime(description='The temporal extent of the resource (start date)'),
    'date_end': fields.DateTime(description='The temporal extent of the resource (end date))'),
    'creation_date': fields.DateTime(description='A point or period of time associated with the creation event \
                    in the lifecycle of the resource'),
    'publication_date': fields.DateTime(description='A point or period of time associated with the publication event \
                    in the lifecycle of the resource'),
    'revision_date': fields.DateTime(description='A point or period of time associated with the revision event  \
                    in the lifecycle of the resource '),

    'resource_locator': fields.String(description='The ‘navigation section’ of a metadata record which point users to the location (URL) \
                    where the data can be downloaded, or to where additional information about the resource may be provided'),
    'license': fields.String(description='Information about resource licensing'),
    'open_dataset': fields.Boolean(description='Used for declaring open datasets.'),
    'topic_category': fields.List(fields.String(description='A high-level classification scheme to assist in the grouping and topic-based \
                    search of available spatial data resources', enum=["Biota", "Boundaries", "Climatology / Meteorology / Atmosphere", "Economy", "Elevation", "Environment",
                    "Farming", "Geoscientific Information", "Health", "Imagery / Base Maps / Earth Cover", "Inland Waters", "Intelligence / Military", "Location", "Oceans",
                    "Planning / Cadastre", "Society", "Structure", "Transportation", "Utilities / Communication"])),
    'reference_system': fields.String(description='Information about the reference system'),
    'spatial_resolution': fields.Integer(description='Spatial resolution refers to the level of detail of the data set'),
    'scales':  fields.List(fields.Nested(scale,description='Scale refers to the level of detail of the data set')),
    'conformity': fields.String(description='Degree of conformity with the implementing rules/standard of the metadata followed', enum=["conformant", "not conformant", "not evaluated"]),
    'conformity_standard': fields.String(description='Title of the implementing rules/standard the resource conforms to'),
    'additional_resources':  fields.List(fields.Nested(additional_resources,description='Auxiliary files or additional resources to the dataset.')),
    'public_access_limitations': fields.String(description='Information on the limitations and the reasons for them'),
    'version': fields.String( description='Version of the resource'),

    'metadata_language': fields.String(description='The language in which the metadata elements are expressed'),
    'metadata_point_of_contact_name': fields.String(description='The name of the organisation responsible for the creation \
                     and maintenance of the metadata'),
    'metadata_point_of_contact_email': fields.String(description='The email of the organisation responsible for the creation \
                     and maintenance of the metadata'),
    'metadata_date': fields.DateTime(description='The date which specifies when the metadata record was created or updated'),
    'metadata_version': fields.String(readOnly=True, description='Version of the metadata record'),

    'use_only_for_vas': fields.Boolean(description='Applicable for vector or raster items'),
    'vetting_required': fields.Boolean(description='Used for customer vetting'),
    'ingestion_info': fields.List(fields.Raw(description='Ingestion information (JSON)')),

    'resources':  fields.List(fields.Nested(resource,description='Provides a list of resources of the dataset.')),
    'lineage': fields.String(description='General explanation of the data producer’s knowledge about the lineage of a dataset'),
    'parent_id': fields.String(description='Provides the ID of a parent dataset.'),
    'parent_data_source_id': fields.String(description='Provides the ID of the parent data source.'),
    'suitable_for': fields.List(fields.String(description='A description of geospatial analysis or processing that the dataset is suitable for')),
    'automated_metadata': fields.List(fields.Raw(description='Automated metadata of the dataset (JSON)')),
    'visibility': fields.List(fields.String(), description='Hidden automated metadata properties'),

    'contract_template_id': fields.Integer(description='The id of the template contract'),
    'contract_template_version': fields.String(description='The version of the template contract'),
    'contract_template_type': fields.String(description='The type of the contract', enum=["MASTER_CONTRACT", "UPLOADED_CONTRACT", "OPEN_DATASET"]),

    'pricing_models': fields.List(fields.Raw(description='Pricing models of the dataset (JSON)')),
    'statistics': fields.Raw(description='Statistics about the store (JSON))'),
    'delivery_method': fields.String(readOnly=True, description='Delivery method of the asset', enum = ["digital_platform", "digital_provider", "physical_provider", "none"]),
    'delivery_method_options': fields.Raw(description='Delivery method options of the item'),
    'versions':  fields.List(fields.String(), description='All versions of the resource'),

    'extensions': fields.Raw(description='Collection of custom properties required for external data provider integration (JSON)'),
})


item_geojson = api.model('the item in geojson format',{
    'id': fields.String(readOnly=True, description='An unambiguous reference to the resource within a given context'),
    'type': fields.String(description='The type of the geojson', default='Feature'),
    'geometry': fields.Nested(polygon, description='The spatial extent of the resource, the spatial \
                    applicability of the resource, or the jurisdiction under which the resource is relevant.', allow_null=True),
    'properties':fields.Nested(properties, description='The properties of the geojson.',required=True)
})

page_of_items = api.model('a page of results', {
    'items': fields.List(fields.Nested(item_geojson, description='Returned geojson objects')),
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

