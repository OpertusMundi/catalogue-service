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


log = logging.getLogger(__name__)

ns = api.namespace('catalogue', description='Operations related to items')

@ns.route('/')
class ItemCollection(Resource):

    @api.response(201, 'Item successfully created.')
    @api.expect(item_geojson)
    def post(self):
        """
        Creates a new item.
        """
        data = request.json
        create_item(data)
        return None, 201


@ns.route('/<string:id>')
@api.response(404, 'Item not found.')
class ItemUnit(Resource):

    #@api.marshal_with(item_geojson)
    def get(self, id):
        """
        Returns a item.
        """
        result = Item.query.filter(Item.id == id).one()
        return result.item_geojson
        if result:
            return marshal(result.item_geojson, item_geojson), 200
        else:
            return {'message': 'No item found'}, 404
        

    @api.expect(item_geojson)
    @api.response(204, 'Item successfully updated.')
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
        return '', 204

    @api.response(204, 'Item successfully deleted.')
    def delete(self, id):
        """
        Deletes a item.
        """
        delete_item(id)
        return None, 204


@ns.route('/search')
@api.response(404, 'Items not found.')
@api.response(200, 'Items found.')
class ItemCollection(Resource):

    @api.expect(search_arguments)
    def get(self):
        """
        Searches and returns a list of items.
        """
        args = search_arguments.parse_args(request)
        log.debug(args)
        q = args.get('q')
        
        items = Item.query.filter(Item.ts_vector.op('@@')(func.plainto_tsquery(q))).all()
        if items:
            result = []
            for i in items:
                result.append(i.item_geojson)
            return result, 200
        else:
            return {'message': 'No items found'}, 404

@ns.route('/get')
@api.response(404, 'Items not found.')
@api.response(200, 'Items found.')
class ItemCollection(Resource):
    @api.expect(id_args)
    def get(self):
        """
        Returns a list of items by ids.
        """
        ids = id_args.parse_args(request).get('id')
        result = []
        for id in ids:
            item = Item.query.filter(Item.id == id).one()
            result.append(item.item_geojson)
        return result, 200