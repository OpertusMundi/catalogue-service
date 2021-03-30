import json
from flask_sqlalchemy import SQLAlchemy

from catalogueapi.database import db
from geoalchemy2.types import Geometry

from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import ARRAY
from shapely.geometry import shape, mapping
from geoalchemy2.shape import to_shape
import shapely.wkt
import datetime
from sqlalchemy.inspection import inspect

from enum import Enum


class ItemModel(db.Model):

    __abstract__ = True

    id = db.Column('id', db.Text, nullable=False, primary_key=True)
    title = db.Column('title', db.Text, nullable=False, index=True)
    abstract = db.Column('abstract', db.Text, index=True)
    type = db.Column('type', db.Text, index=True)

    spatial_data_service_type = db.Column(
        'spatial_data_service_type', db.Text, index=True)
    spatial_data_service_version = db.Column(
        'spatial_data_service_version', db.Text, index=True)
    spatial_data_service_operations = db.Column('spatial_data_service_operations', ARRAY(db.Text), index=True)
    spatial_data_service_queryables = db.Column('spatial_data_service_queryables', ARRAY(db.Text), index=True)


    format = db.Column('format', db.Text, index=True)
    keywords = db.Column('keywords', ARRAY(JSONB), index=True)
    publisher_name = db.Column('publisher_name', db.Text, index=True)
    publisher_email = db.Column('publisher_email', db.Text, index=True)
    publisher_id = db.Column('publisher_id', db.Text, index=True)
    language = db.Column('language', db.Text, index=True)
    date_start = db.Column('date_start', db.Date, index=True)
    date_end = db.Column('date_end', db.Date, index=True)
    creation_date = db.Column('creation_date', db.Date, index=True)
    publication_date = db.Column('publication_date', db.Date, index=True)
    revision_date = db.Column('revision_date', db.Date, index=True)

    geographic_location = db.Column('geographic_location', Geometry(
        geometry_type='POLYGON'), index=True)

    resource_locator = db.Column('resource_locator', db.Text, index=True)
    license = db.Column('license', db.Text, index=True)
    topic_category = db.Column('topic_category', ARRAY(db.Text), index=True)

    reference_system = db.Column('reference_system', db.Text, index=True)
    spatial_resolution = db.Column('spatial_resolution', db.Integer, index=True)
    scales = db.Column('scale', ARRAY(JSONB), index=True)
    version = db.Column('version', db.Text, index=True)
    conformity = db.Column('conformity', db.Text, index=True)
    additional_resources = db.Column(
        'additional_resources', ARRAY(JSONB), index=True)
    public_access_limitations = db.Column(
        'public_access_limitations', db.Text, index=True)

    metadata_language = db.Column('metadata_language', db.Text, index=True)
    metadata_point_of_contact_name = db.Column(
        'metadata_point_of_contact_name', db.Text, index=True)
    metadata_point_of_contact_email = db.Column(
        'metadata_point_of_contact_email', db.Text, index=True)
    metadata_date = db.Column('metadata_date', db.Date, index=True)
    metadata_version = db.Column('metadata_version', db.Text, index=True)
    resources = db.Column('resources', ARRAY(JSONB), index=True)
    lineage = db.Column('lineage', db.Text, index=True)
    parent_id = db.Column('parent_id', db.Text, index=True)

    item_geojson = db.Column('item_geojson', JSONB)

    pricing_models = db.Column('pricing_models', JSONB)
    statistics = db.Column('statistics', JSONB)
    delivery_method = db.Column('delivery_method', db.Text, index=True)

    responsible_party = db.Column('responsible_party', JSONB)

    automated_metadata = db.Column('automated_metadata', JSONB)

    harvested_from = db.Column('harvested_from', db.Text, index=True)
    harvest_json = db.Column('harvest_json', JSONB)

    use_only_for_vas = db.Column('use_only_for_vas', db.Boolean, default=False, index=True)
    ingestion_info = db.Column('ingestion_info', JSONB)

    created_at = db.Column('created_at', db.Date, index=True)
    submitted_at = db.Column('submitted_at', db.Date, index=True)
    accepted_at = db.Column('accepted_at', db.Date, index=True)

    visibility = db.Column('visibility', ARRAY(db.Text), index=True)

    suitable_for = db.Column('suitable_for', ARRAY(db.Text), index=True)

    ts_vector = func.to_tsvector('english', item_geojson)

    def update(self, id, data):
        properties = data.get('properties')
        if data.get('geometry') is not None:
            geom = data['geometry']
            self.geographic_location = shape(geom).wkt
        for key in properties:
            if properties[key] is not None:
                setattr(self, key, properties[key])
        self.id = id
        item_geojson = self.serialize()
        self.item_geojson = item_geojson
        return

    # convert to geojson format
    def serialize(self):
        # build properties object
        p = {}
        geom = None
        for c in inspect(self).attrs.keys():
            attr = getattr(self, c)
            if c == 'geographic_location' and attr is not None:
                # Convert to a shapely Polygon object to get mapping
                if isinstance(attr, str):
                    g = shapely.wkt.loads(attr)
                    geom = mapping(g)
                else:
                    g = to_shape(attr)
                    geom = mapping(g)

            elif isinstance(attr, datetime.date):
                p[c] = attr.isoformat()
            elif c == 'id' or c == 'item_geojson':
                continue
            else:
                p[c] = attr
        # build geojson
        item_geojson = \
            {
                "id": self.id,
                "type": "Feature",
                "geometry": geom,
                "properties": p
            }
        return item_geojson


class Item(ItemModel):
    __tablename__ = "item"

    __table_args__ = (
        db.Index(
            'item_index',
            ItemModel.ts_vector,
            postgresql_using='gin'
        ),
    )


class Draft(ItemModel):
    __tablename__ = "draft"

    status = db.Column(
        'status', db.Enum('draft', 'review', 'accepted', 'embargo', name="status"), index=True)

    __table_args__ = (
        db.Index(
            'draft_index',
            ItemModel.ts_vector,
            postgresql_using='gin'
        ),
    )


class History(ItemModel):
    __tablename__ = "history"

    version_id = db.Column('version_id', db.Integer,
                           primary_key=True, autoincrement=True)

    deleted = db.Column('deleted', db.Boolean, index=True)

    deleted_at = db.Column('deleted_at', db.Date, index=True)

    __table_args__ = (
        db.Index(
            'history_index',
            ItemModel.ts_vector,
            postgresql_using='gin'
        ),
    )

class Harvest(ItemModel):
    __tablename__ = "harvest"

    __table_args__ = (
        db.Index(
            'harvested_index',
            ItemModel.ts_vector,
            postgresql_using='gin'
        ),
    )
