import logging
import json

from flask import request
from flask_restx import Resource
from flask_restx import marshal
from catalogueapi.database.actions.item import create_item, delete_item, update_item
from catalogueapi.api.serializers import item_geojson, page_of_items
from catalogueapi.api.parsers import pagination_arguments, search_arguments, id_args
from catalogueapi.api.restx import api
from catalogueapi.database.model.item import Item
from sqlalchemy.sql import func
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

ns = api.namespace('catalogue', description='Operations related to items')

@ns.route('/')
class ItemCollection(Resource):

    @api.response(200, 'Item successfully created.')
    @api.expect(item_geojson)
    def post(self):
        """
        Creates a new item.
        """
        data = request.json
        create_item(data)
        return {'success': True, 'message': {'code':200, 'description':'Item successfully created.' } }, 200


@ns.route('/<string:id>')
@api.response(404, 'Item not found.')
@api.response(200, 'Item found.')
class ItemUnit(Resource):

    def get(self, id):
        """
        Returns an item.
        """
        
        try:
            result = Item.query.filter(Item.id == id).one()
        except NoResultFound:
            return {'success': False, 'message': {'code':404, 'description':'No items found' } }, 404
        return {'result': marshal(result.item_geojson, item_geojson), 'success': True, 'message':
                     {'code':200, 'description': 'Item found' } }, 200
        

    @api.expect(item_geojson)
    @api.response(200, 'Item successfully updated.')
    def put(self, id):
        """
        Updates a item.
        Use this method to change a property of an item.
        * Send a geojson object with the new values in the request body.
        ```
        {
         "properties": {
            "title": "New item title"
          }
        }
        ```
        * Specify the ID of the item to modify in the request URL path.
        """
        data = request.json
        update_item(id, data)
        return '', 200

    @api.response(200, 'Item successfully deleted.')
    def delete(self, id):
        """
        Deletes a item.
        """
        delete_item(id)
        return None, 200


@ns.route('/search')
@api.response(404, 'No items found for this query')
@api.response(200, 'Items found')
class ItemCollection(Resource):

    #@api.marshal_list_with(page_of_items)
    @api.expect(search_arguments, validate=False)
    def get(self):
        """
        Searches and returns a list of items.
        """
        args = search_arguments.parse_args(request)
        q = args.get('q')
        page = args.get('page')
        per_page = args.get('per_page')
        items = Item.query.filter(Item.ts_vector.op('@@')(func.plainto_tsquery(q)))
        result = items.paginate(page, per_page, error_out=False)
        items_geojson = []
        if result.items:
            for i in result.items:
                items_geojson.append(i.item_geojson)
            result.items = items_geojson
            return {'result': marshal(result, page_of_items), 'success': True, 'message':
                     {'code':200, 'description': 'Items found' } }, 200
        else:
            return {'success': False, 'message': {'code':404, 'description':'No items found for this query' } }, 404


@ns.route('/get')
@api.response(404, 'No items found with those ids')
@api.response(200, 'Items found')
class ItemCollection(Resource):
    @api.expect(id_args)
    def get(self):
        """
        Returns a list of items by ids.
        """
        ids = id_args.parse_args(request).get('id')
        result = []
        for id in ids:
            try:
                item = Item.query.filter(Item.id == id).one()
                result.append(item.item_geojson)
            except NoResultFound:
                continue
        if result:
            return {'result': result, 'success': True, 'message':
                     {'code':200, 'description': 'Items found' } }, 200
        else:
            return {'success': False, 'message': {'code':404, 'description':'No items found with those ids' } }, 404
