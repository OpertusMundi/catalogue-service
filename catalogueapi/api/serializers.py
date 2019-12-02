from flask_restplus import fields
from catalogueapi.api.restplus import api

item = api.model('A simple item', {
    'item_id': fields.String(readOnly=True, description='The unique identifier of an item'),
    'title': fields.String(required=True, description='The title of the item'),
    'description': fields.String(description='A short description'),
    'creator': fields.String(description='The creator of the item')
})