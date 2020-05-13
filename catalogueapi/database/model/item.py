import json
from flask_sqlalchemy import SQLAlchemy

from catalogueapi.database import db
from geoalchemy2.types import Geometry


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column('id', db.Text, primary_key=True)
    title = db.Column('title', db.Text, nullable=False, index=True)
    description = db.Column('description', db.Text, index=True)
    type = db.Column('type', db.Text, index=True)
    spatial_data_service_type = db.Column(
        'spatial_data_service_type', db.Text, index=True)
    format = db.Column('format', db.Text, index=True)
    keywords = db.Column('keywords', db.Text, index=True)
    publisher = db.Column('publisher', db.Text, index=True)
    language = db.Column('language', db.Text, index=True)
    publication_date = db.Column('publication_date', db.Date, index=True)
    revision_date = db.Column('revision_date', db.Date, index=True)

    geographic_location = db.Column('geographic_location', Geometry(
        geometry_type='POLYGON', srid=4326), index=True)
    date_start = db.Column('date_start', db.Date, index=True)
    date_end = db.Column('date_end', db.Date, index=True)
    resource_locator = db.Column('resource_locator', db.Text, index=True)

    license = db.Column('license', db.Text, index=True)
    topic_category = db.Column('topic_category', db.Text, index=True)

    reference_system = db.Column('reference_system', db.Text, index=True)
    spatial_resolution = db.Column('spatial_resolution', db.Text, index=True)
    version = db.Column('version', db.Text, index=True)
    conformity = db.Column('conformity', db.Text, index=True)
    additional_resources = db.Column(
        'additional_resources', db.Text, index=True)
    public_access_limitations = db.Column(
        'public_access_limitations', db.Text, index=True)

    metadata_language = db.Column('metadata_language', db.Text, index=True)
    metadata_point_of_contact = db.Column(
        'metadata_point_of_contact', db.Text, index=True)
    metadata_date = db.Column('metadata_date', db.Date, index=True)
    coupled_resource = db.Column('coupled_resource', db.Text, index=True)
    lineage = db.Column('lineage', db.Text, index=True)
    parent_id = db.Column('parent_id', db.Text, index=True)

    item_json = db.Column('item_json', db.JSON)

    def __init__(self, data):
        self.id = data.get('id')
        self.title = data.get('title')
        self.description = data.get('description')
        self.item_json = data
