import logging
import json

from flask import request
from flask_restx import Resource
from flask_restx import marshal
from catalogueapi.database.actions.item import create_item, delete_item, update_item
from catalogueapi.api.serializers import item, page_of_items
from catalogueapi.api.parsers import pagination_arguments, search_arguments
from catalogueapi.api.restx import api
from catalogueapi.database.model.item import Item

from sqlalchemy.sql import func


log = logging.getLogger(__name__)

ns = api.namespace('items', description='Operations related to items')

@ns.route('/')
class ItemCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_list_with(page_of_items)
    def get(self):
        """
        Returns a list of items.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page')
        per_page = args.get('per_page')
        items = Item.query
        results = items.paginate(page, per_page, error_out=False)
        return results

    @api.response(201, 'Item successfully created.')
    @api.expect(item)
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

    @api.marshal_with(item)
    def get(self, id):
        """
        Returns a item.
        """
        return Item.query.filter(Item.id == id).one()
        

    @api.expect(item)
    @api.response(204, 'Item successfully updated.')
    def put(self, id):
        """
        Updates a item.
        Use this method to change a property of an item.
        * Send a JSON object with the new value in the request body.
        ```
        {
          "name": "New item Name"
        }
        ```
        * Specify the ID of the item to modify in the request URL path.
        """
        data = request.json
        update_item(id, data)
        return None, 204

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
        Returns a list of items.
        """
        args = search_arguments.parse_args(request)
        log.debug(args)
        q = args.get('q')
        
        items = Item.query.filter(Item.ts_vector.op('@@')(func.plainto_tsquery(q))).all()
        if items:
            return marshal(items, item), 200
        else:
            return {'message': 'No items found'}, 404

