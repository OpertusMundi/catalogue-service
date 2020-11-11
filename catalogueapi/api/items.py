import logging
import json

from flask import request
from flask_restx import Resource
from flask_restx import marshal
from catalogueapi.database.actions.item import create_item, delete_item, update_item, \
    create_draft, create_draft_from_item, update_status, update_draft
from catalogueapi.api.serializers import item_geojson, page_of_items
from catalogueapi.api.parsers import pagination_args, pub_search_args, draft_search_args, id_args, update_status_args
from catalogueapi.api.restx import api
from catalogueapi.database.model.item import Item, Draft
from sqlalchemy.sql import func
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

ns = api.namespace('catalogue', description='Operations related to items')


@ns.route('/draft/create')
class ItemCollection(Resource):
    @api.response(200, 'Item successfully created.')
    @api.expect(item_geojson)
    def post(self):
        """
        Creates a new item (draft).
        """
        data = request.json
        id = create_draft(data)

        return {
            'success': True,
            'message': {
                'code': 200,
                'description': 'Item successfully created.'
            }
        }, 200


@ns.route('/draft/create_from_published/<string:id>')
class ItemCollection(Resource):
    @api.response(200, 'Draft successfully created.')
    def post(self, id):
        """
        Creates a new draft from an existing published item.
        """
        create_draft_from_item(id)

        return {
            'success': True,
            'message': {
                'code': 200,
                'description': 'Draft successfully created.'
            }
        }, 200


@ns.route('/draft/update_status')
class Status(Resource):
    @api.expect(update_status_args, validate=False)
    @api.response(200, 'Status successfully updated.')
    def put(self):
        """
        Updates a draft's status.
        """
        id = update_status_args.parse_args(request).get('id')
        status = update_status_args.parse_args(request).get('status')
        update_status(id, status)
        return {
            'success': True,
            'message': {
                'code': 200,
                'description': 'Status successfully updated.'
            }
        }, 200


@ns.route('/published/<string:id>')
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
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'No items found'
                }
            }, 404
        return {
            'result': result.item_geojson,
            'success': True,
            'message': {
                'code': 200,
                'description': 'Item found'
            }
        }, 200

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
        return 'Item successfully updated.', 200

    @api.response(200, 'Item successfully deleted.')
    def delete(self, id):
        """
        Deletes a item.
        """
        delete_item(id)
        return None, 200


@ns.route('/draft/<string:id>')
@api.response(404, 'Item not found.')
@api.response(200, 'Item found.')
class ItemUnit(Resource):
    def get(self, id):
        """
        Returns a draft.
        """

        try:
            result = Draft.query.filter(Draft.id == id).one()
        except NoResultFound:
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'No drafts found'
                }
            }, 404
        return {
            'result': result.item_geojson,
            'success': True,
            'message': {
                'code': 200,
                'description': 'Draft found'
            }
        }, 200

    @api.expect(item_geojson)
    @api.response(200, 'Draft successfully updated.')
    def put(self, id):
        """
        Updates a draft.
        Use this method to change a property of a draft.
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
        update_draft(id, data)
        return 'Item successfully updated.', 200

    @api.response(200, 'Item successfully deleted.')
    def delete(self, id):
        """
        Deletes a item.
        """
        delete_draft(id)
        return None, 200


@ns.route('/published/search')
@api.response(404, 'No items found for this query')
@api.response(200, 'Items found')
class ItemCollection(Resource):

    #@api.marshal_list_with(page_of_items)
    @api.expect(pub_search_args, validate=False)
    def get(self):
        """
        Searches and returns a list of items.
        """
        args = pub_search_args.parse_args(request)

        publisher_id = args.get('publisher_id')
        q = args.get('q')
        bbox = args.get('bbox')
        time = args.get('time')
        page = args.get('page')
        per_page = args.get('per_page')

        # Initialize items query
        items = Item.query

        # Search by publisher
        if publisher_id:
            items = items.filter(Item.publisher_id == publisher_id)

        # Add filtering (optional)
        if q and q.strip() != "":
            items = items.filter(
                Item.ts_vector.op('@@')(func.plainto_tsquery(q)))

        # Spatial query
        if bbox:
            xmin, ymin, xmax, ymax = bbox.split(',')
            bbox_polygon = 'POLYGON (({0} {1}, {0} {3}, {2} {3}, {2} {1}, {0} {1} ))'.format(
                xmin, ymin, xmax, ymax)
            items = items.filter(
                Item.geographic_location.ST_Within(bbox_polygon))

        # Time extent
        if time:
            time_start, time_end = time.split('/')
            items = items.filter(Item.date_start >= time_start).filter(
                Item.date_end <= time_end)

        # Add pagination
        result = items.paginate(page, per_page, error_out=False)

        items_geojson = []

        # Post-process to get item_geojson
        if result.items:
            for i in result.items:
                items_geojson.append(i.item_geojson)
            result.items = items_geojson
            return {
                'result': result.items,
                'success': True,
                'message': {
                    'code': 200,
                    'description': 'Items found'
                }
            }, 200
        else:
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'No items found for this query'
                }
            }, 404


@ns.route('/draft/search')
@api.response(404, 'No drafts found for this query')
@api.response(200, 'Drafts found')
class DraftCollection(Resource):

    #@api.marshal_list_with(page_of_items)
    @api.expect(draft_search_args, validate=False)
    def get(self):
        """
        Searches and returns a list of drafts.
        """
        args = draft_search_args.parse_args(request)

        publisher_id = args.get('publisher_id')
        status = args.get('status')
        page = args.get('page')
        per_page = args.get('per_page')
        # Initialize items query
        drafts = Draft.query

        # Search by publisher
        if publisher_id:
            drafts = drafts.filter(Draft.publisher_id == publisher_id)

        # Search by status
        if status:
            drafts = drafts.filter(Draft.status == status)

        # Add pagination
        result = drafts.paginate(page, per_page, error_out=False)

        items_geojson = []

        # Post-process to get item_geojson
        if result.items:
            for i in result.items:
                items_geojson.append(i.item_geojson)
            result.items = items_geojson

            log.info('Result %s', result)
            return {
                'result': marshal(result, page_of_items),
                'success': True,
                'message': {
                    'code': 200,
                    'description': 'Items found'
                }
            }, 200
        else:
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'No items found for this query'
                }
            }, 404


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
            return {
                'result': result,
                'success': True,
                'message': {
                    'code': 200,
                    'description': 'Items found'
                }
            }, 200
        else:
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'No items found with those ids'
                }
            }, 404
