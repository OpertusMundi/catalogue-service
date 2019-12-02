import logging

from flask import request
from flask_restplus import Resource
from catalogueapi.database.actions.item import create_item, delete_item, update_item
from catalogueapi.api.serializers import item
from catalogueapi.api.restplus import api
from catalogueapi.database.model.item import Item

log = logging.getLogger(__name__)

ns = api.namespace('items', description='Operations related to items')


@ns.route('/')
class ItemCollection(Resource):

    @api.marshal_list_with(item)
    def get(self):
        """
        Returns list of items.
        """
        items = Item.query.all()
        return items

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
        Use this method to change the name of a item.
        * Send a JSON object with the new name in the request body.
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


