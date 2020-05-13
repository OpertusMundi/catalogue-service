from flask_restx import fields
from catalogueapi.api.restx import api

item = api.model('A simple item', {
    'id': fields.String(readOnly=True, description='The unique identifier of an item'),
    'title': fields.String(required=True, description='The title of the item'),
    'description': fields.String(description='A short description'),
    'creator': fields.String(description='The creator of the item')
})

page_of_items = api.model('A page of results', {
    'items': fields.List(fields.Nested(item)),
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
    })