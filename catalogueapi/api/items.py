import requests
import logging
import json

from flask import request, current_app
from flask_restx import Resource
from flask_restx import marshal
import catalogueapi.database.actions.item as actions
from catalogueapi.database.actions.harvest import harvest
from catalogueapi.api.serializers import item_geojson, page_of_items, list_of_pairs
import catalogueapi.api.parsers as p
from catalogueapi.api.restx import api
from catalogueapi.database.model.item import Asset_in_bundle, Item, Draft, History, Harvest
from catalogueapi.api.helpers import convert_from_iso
from sqlalchemy.sql import func
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from owslib.iso import *

ns = api.namespace('', description='Operations related to items')

@ns.route('/draft/create')
class ItemCollection(Resource):
    @api.response(200, 'Draft successfully created.')
    @api.response(400, 'Error creating draft.')
    @ns.expect(item_geojson)
    def post(self):
        """
        Creates a new item (draft).
        """
        data = request.json
        # validate input first
        try:
            actions.validate_input(data)
            id = actions.create_draft(data)
        except Exception as ex:
            current_app.logger.error('Error creating draft: ' + str(ex))
            return {
                'success': False,
                'message': {
                    'code': 400,
                    'description': str(ex)
                }
            }, 400


        return {
            'success': True,
            'message': {
                'code': 200,
                'description': 'Draft successfully created.'
            }
        }, 200


@ns.route('/draft/status')
class Status(Resource):
    @api.expect(p.update_status_args, validate=False)
    @api.response(200, 'Status successfully updated.')
    @api.response(400, 'Error updating status.')
    @api.response(404, 'Draft not found.')
    def put(self):
        """
        Updates a draft's status.
        """
        id = p.update_status_args.parse_args(request).get('id')
        status = p.update_status_args.parse_args(request).get('status')
        current_app.logger.info('Updating status of draft ' + id)
        try:
            actions.update_status(id, status)
        except NoResultFound:
            current_app.logger.error('Draft {} not found.'.format(id))
            return{
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'Draft {} not found.'.format(id)
                }
            }, 404
        except Exception as ex:
            current_app.logger.error('Error updating status: ' + str(ex))
            return{
                'success': False,
                'message': {
                    'code': 400,
                    'description': 'Error updating status.' + str(ex)
                }
            }, 400
        return {
            'success': True,
            'message': {
                'code': 200,
                'description': 'Status successfully updated.'
            }
        }, 200


@api.response(404, 'Item not found.')
@ns.route('/published/<string:id>')
class ItemUnit(Resource):

    @api.response(200, 'Item found.', item_geojson)
    def get(self, id):
        """
        Returns a published item (including a list of all versions).
        """

        try:
            result = Item.query.filter(Item.id == id).one()
        except NoResultFound:
            current_app.logger.error('No items found')
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'No items found'
                }
            }, 404

        # include previous versions (sorted from newest to latest version)
        try:
            history = History.query.filter(History.id == id).order_by((History.metadata_version).desc())
        except Exception as ex:
            current_app.logger.error('Error getting published item and all versions:  ' + str(ex))
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'Error getting published item and all versions: ' + str(ex)
                }
            }, 404
        versions = [result.version]
        for h in history:
            if h.version not in versions:
                versions.append(h.version)
        result.item_geojson['properties']['versions'] = versions
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
        item = Item.query.filter(Item.id == id).one()
        actions.update_item(item, data)
        return 'Item successfully updated.', 200

    @api.response(200, 'Item successfully deleted.')
    @api.response(400, 'Delete failed')
    def delete(self, id):
        """
        Deletes a item.
        """
        try:
            actions.delete_item(id)
        except Exception as ex:
            current_app.logger.error('Delete failed: ' + str(ex))
            return {
                'success': False,
                'message': {
                    'code': 400,
                    'description': 'Delete failed: ' + str(ex)
                }
            }, 404
        return {
            'success': True,
            'message': {
                'code': 200,
                'description': 'Item successfully deleted.'
            }
        }, 200


@ns.route('/draft/<string:id>')
class ItemUnit(Resource):
    @api.response(404, 'Published item not found.')
    @api.response(200, 'Draft successfully created.')
    def post(self, id):
        """
        Creates a new draft from an existing published item.
        """
        try:
            item = Item.query.filter(Item.id == id).one()
            actions.create_draft_from_item(item)
        except NoResultFound:
            current_app.logger.error('Published item {} not found'.format(id))
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'Published item {} not found.'.format(id)
                }
            }, 404
        except IntegrityError:
            current_app.logger.error('Draft for this published item already exists')
            return {
                'success': False,
                'message': {
                    'code': 400,
                    'description': 'Draft for this published item already exists.'
                }
            }, 400
        except Exception as ex:
            current_app.logger.error('Draft creation failed: ' + str(ex))
            return {
                'success': False,
                'message': {
                    'code': 400,
                    'description': 'Draft creation failed: ' + str(ex)
                }
            }, 400
        return {
            'success': True,
            'message': {
                'code': 200,
                'description': 'Draft successfully created.'
            }
        }, 200

    @api.response(404, 'Draft not found.')
    @api.response(200, 'Draft found.', item_geojson)
    def get(self, id):
        """
        Returns a draft.
        """

        try:
            result = Draft.query.filter(Draft.id == id).one()
        except NoResultFound:
            current_app.logger.error('Draft not found')
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'Draft not found.'
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
    @api.response(404, 'Draft not found')
    @api.response(400, 'Error updating draft.')
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
        try:
            draft = Draft.query.filter(Draft.id == id).one()
            actions.update_draft(draft, data)
        except NoResultFound:
            current_app.logger.error('Draft not found')
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'Draft not found.'
                }
            }, 404
        except Exception as ex:
            current_app.logger.error('Error updating draft: ' + str(ex))
            return {
                'success': False,
                'message': {
                    'code': 400,
                    'description': 'Error updating draft: ' + str(ex)
                }
            }, 400
        return {
            'success': True,
            'message': {
                'code': 200,
                'description': 'Draft successfully updated.'
            }
        }, 200

    @api.response(400, 'Draft delete failed')
    @api.response(200, 'Draft successfully deleted.')
    def delete(self, id):
        """
        Deletes a draft.
        """
        try:
            actions.delete_draft(id)
        except Exception as ex:
            current_app.logger.error('Draft delete failed: ' + str(ex))
            return {
                'success': False,
                'message': {
                    'code': 400,
                    'description': 'Draft delete failed: ' + str(ex)
                }
            }, 400
        return {
            'success': True,
            'message': {
                'code': 200,
                'description': 'Draft successfully deleted.'
            }
        }, 200

@ns.route('/harvest/<string:id>')
class HarvestUnit(Resource):

    @api.response(200, 'Harvested item found.', item_geojson)
    def get(self, id):
        """
        Returns a harvested item
        """

        try:
            result = Harvest.query.filter(Harvest.id == id).one()
        except NoResultFound:
            current_app.logger.error('Harvested item not found')
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'Harvested item not found.'
                }
            }, 404
        return {
            'result': result.item_geojson,
            'success': True,
            'message': {
                'code': 200,
                'description': 'Harvested item found'
            }
        }, 200

    @api.expect(item_geojson)
    @api.response(200, 'Harvested item successfully updated.')
    def put(self, id):
        """
        Updates a harvested item.
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
        harvest = Harvest.query.filter(Harvest.id == id).one()
        actions.update_harvested_item(harvest, data)
        return 'Item successfully updated.', 200

    @api.response(200, 'Harvested item successfully deleted.')
    @api.response(404, 'Harvested item not found.')
    def delete(self, id):
        """
        Deletes a harvested item.
        """
        try:
            actions.delete_harvested_item(id)
        except Exception as ex:
            current_app.logger.error('Harvested item delete failed: ' + str(ex))
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'Harvested item delete faled: ' + str(ex)
                }
            }, 404
        return {
            'success': True,
            'message': {
                'code': 200,
                'description': 'Harvested item successfully deleted.'
            }
        }, 200

@ns.route('/history/get')
class ItemUnit(Resource):
    @api.response(404, 'Version was not found.')
    @api.response(200, 'Version was found.',item_geojson)
    @api.expect(p.history_get_args)
    def get(self):
        """
        Returns a specific version of an item.
        """

        id = p.history_get_args.parse_args(request).get('id')
        version = p.history_get_args.parse_args(request).get('version')
        
        result = History.query.filter(History.id == id).filter(History.version == version).all()
        if result:
            # select latest metadata version
            latest_item =  result[0]
            latest_version = int(latest_item.metadata_version.split('.')[-1])
            for item in result:
                vers = int(item.metadata_version.split('.')[-1])
                if vers > latest_version:
                    latest_version = vers
                    latest_item = item
            result = latest_item
        else:   
            # search in published
            try: 
                result =  Item.query.filter(Item.id == id).filter(Item.version == version).one()
            except NoResultFound:
                current_app.logger.error('Item version was not found: ')
                return {
                    'success': False,
                    'message': {
                        'code': 404,
                        'description': 'Item version was not found.'
                    }
                }, 404

        return {
            'result': result.item_geojson,
            'success': True,
            'message': {
                'code': 200,
                'description': 'Item version found'
            }
        }, 200

@ns.route('/history/get_list')
class ItemUnit(Resource):
    @api.response(404, 'Versions of the items were found.')
    @api.response(200, 'Version of the items were not found.')
    @api.expect(list_of_pairs)
    def post(self):
        """
        Returns a specific version for each item id and version pair.
        """

        id_version_pairs = request.json.get('id_version_pairs')
        item_list = []
        for i in id_version_pairs:
            query = History.query.filter(History.id == i.get('id'))

            if not i.get('version') is None and len(i.get('version')) != 0:
                query = query.filter(History.version == i.get('version'))

            result = query.all()
            if result:
                # select latest metadata version
                latest_item =  result[0]
                latest_version = int(latest_item.metadata_version.split('.')[-1])
                for item in result:
                    vers = int(item.metadata_version.split('.')[-1])
                    if vers > latest_version:
                        latest_version = vers
                        latest_item = item
                result = latest_item
                item_list.append(result.item_geojson)
            else:   
                # search in published
                try: 
                    result =  Item.query.filter(Item.id == i.get('id')).filter(Item.version == i.get('version')).one()
                    item_list.append(result.item_geojson)
                except NoResultFound:
                    continue
            
        if item_list:
            return {
                'result': item_list,
                'success': True,
                'message': {
                    'code': 200,
                    'description': 'Versions of the items were found.'
                }
            }, 200
        else:
            return {
                    'success': False,
                    'message': {
                        'code': 404,
                        'description': 'Versions of the items were not found.'
                    }
                }, 404

@ns.route('/published/search')
@api.response(404, 'No items found for this query')
@api.response(200, 'Items found', page_of_items)
class ItemCollection(Resource):

    # @api.marshal_list_with(page_of_items)
    @api.expect(p.pub_search_args, validate=False)
    def get(self):
        """
        Searches and returns a list of items.
        """
        args = p.pub_search_args.parse_args(request)

        publisher_id = args.get('publisher_id')
        type = args.get('type')
        q = args.get('q')
        bbox = args.get('bbox')
        orderBy = args.get('orderBy')
        order = args.get('order')
        time = args.get('time')
        page = args.get('page')
        per_page = args.get('per_page')

        # Initialize items query
        items = Item.query

        # Search by publisher
        if publisher_id:
            items = items.filter(Item.publisher_id == publisher_id)

        # Search by asset type
        if type:
            lc_type = [x.lower() for x in type]
            items = items.filter(Item.type.in_(lc_type))

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

        # Order by 
        if orderBy == 'TITLE':
            items = items.order_by((Item.title).asc()) if order=='ASC' else items.order_by((Item.title).desc())
        elif orderBy == 'DATE_PUBLISHED':
            items = items.order_by((Item.publication_date).asc()) if order=='ASC' else items.order_by((Item.publication_date).desc())
        elif orderBy == 'TYPE':
            items = items.order_by((Item.type).asc()) if order=='ASC' else items.order_by((Item.type).desc()) 

        # Add pagination
        result = items.paginate(page, per_page, error_out=False)

        items_geojson = []
        # Post-process to get item_geojson
        if result.items:
            for i in result.items:
                items_geojson.append(i.item_geojson)
            result.items = items_geojson
            return {
                'result':  marshal(result, page_of_items),
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
@api.response(200, 'Drafts found', page_of_items)
class DraftCollection(Resource):

    # @api.marshal_list_with(page_of_items)
    @api.expect(p.draft_search_args, validate=False)
    def get(self):
        """
        Searches and returns a list of drafts.
        """
        args = p.draft_search_args.parse_args(request)

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
            drafts = drafts.filter(Draft.status.in_(status))

        # Add pagination
        result = drafts.paginate(page, per_page, error_out=False)

        items_geojson = []

        # Post-process to get item_geojson
        if result.items:
            for i in result.items:
                items_geojson.append(i.item_geojson)
            result.items = items_geojson

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


@ns.route('/published/get')
@api.response(404, 'No items found with those ids')
@api.response(200, 'Items found')
class ItemCollection(Resource):
    @api.expect(p.id_args)
    def get(self):
        """
        Returns a list of items by ids.
        """
        ids = p.id_args.parse_args(request).get('id')
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

@ns.route('/published/related_items/<string:id>')
@api.response(404, 'No related items found for this id')
@api.response(200, 'Related items found')
class ItemCollection(Resource):
    def get(self, id):
        """
        Returns a list of items (parent, siblings and children excluding self)
        """
        
        item = Item.query.filter(Item.id == id).one()
        parent_id = item.parent_id
        result = []
        try:
            children = Item.query.filter(Item.parent_id == id).all()
            for c in children:
                if c.id != id:
                    result.append(c.item_geojson)
        except:
            pass
        if parent_id:
            try:
                siblings = Item.query.filter(Item.parent_id == parent_id).all()
                for s in siblings:
                    if s.id != id:
                        result.append(s.item_geojson)
            except NoResultFound:
                pass
            try:
                parent = Item.query.filter(Item.id == parent_id).one()
                result.append(parent.item_geojson)
            except NoResultFound:
                pass

        if result:
            return {
                'result': result,
                'success': True,
                'message': {
                    'code': 200,
                    'description': 'Related items found'
                }
            }, 200
        else:
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'No related items found for this id'
                }
            }, 404

@ns.route('/published/related_data_source_items/<string:id>')
@api.response(404, 'No items found for this parent data source id')
@api.response(200, 'Items found for this parent data source id')
class ItemCollection(Resource):
    def get(self, id):
        """
        Returns a list of items with the requested parent data source id
        """
        
        items = Item.query.filter(Item.parent_data_source_id == id).all()
        result = []

        if items:
            for i in items:
                result.append(i.item_geojson) 
            return {
                'result': result,
                'success': True,
                'message': {
                    'code': 200,
                    'description': 'Items found for this parent data source id'
                }
            }, 200
        else:
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'No items found for this parent data source id'
                }
            }, 404       

@ns.route('/published/available_as/<string:id>')
@api.response(404, 'Asset not found available in any bundles')
@api.response(400, 'Error searching for bundles')
@api.response(200, 'Asset found available in a bundle')
class ItemCollection(Resource):
    def get(self, id):
        """
        Returns a list of bundles asset is part of
        """
        
        try:
            bundles = Asset_in_bundle.query.filter(Asset_in_bundle.asset_id == id).all()
            result = []
            for b in bundles:
                item = Item.query.filter(Item.id == b.bundle_id).all()
                if item: result.append(item[0].item_geojson)
        except Exception as ex:
            current_app.logger.error('Error searching for bundles: ' + str(ex))
            return {
                'success': False,
                'message': {
                    'code': 400,
                    'description': 'Error searching for bundles: ' + str(ex)
                }
            }, 400

        if result:
            return {
                'result': result,
                'success': True,
                'message': {
                    'code': 200,
                    'description': 'Asset found available in a bundle'
                }
            }, 200
        else:
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'Asset not found available in any bundles'
                }
            }, 404



@ns.route('/history/search')
@api.response(404, 'No items found for this query')
@api.response(200, 'Items found', page_of_items)
class DraftCollection(Resource):

    # @api.marshal_list_with(page_of_items)
    @api.expect(p.history_search_args, validate=False)
    def get(self):
        """
        Searches and returns a list of drafts.
        """
        args = p.history_search_args.parse_args(request)

        item_id = args.get('item_id')
        publisher_id = args.get('publisher_id')
        deleted = args.get('deleted')
        page = args.get('page')
        per_page = args.get('per_page')
        # Initialize items query
        history = History.query

        # Search by item id
        if item_id:
            history = history.filter(History.id == item_id)

        # Search by publisher
        if publisher_id:
            history = history.filter(History.publisher_id == publisher_id)

        # Search by status
        if deleted:
            history = history.filter(History.deleted == deleted)


        # Add pagination
        result = history.paginate(page, per_page, error_out=False)

        items_geojson = []

        # Post-process to get item_geojson
        if result.items:
            for i in result.items:
                items_geojson.append(i.item_geojson)
            result.items = items_geojson

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

@ns.route('/harvest/search')
@api.response(404, 'No items found from this url')
@api.response(200, 'Items found', page_of_items)
class HarvestCollection(Resource):

    # @api.marshal_list_with(page_of_items)
    @api.expect(p.harvest_search_args, validate=False)
    def get(self):
        """
        Searches and returns a list of harvests.
        """
        args = p.harvest_search_args.parse_args(request)

        harvest_url = args.get('harvest_url')
        q = args.get('q')
        page = args.get('page')
        per_page = args.get('per_page')
        # Initialize items query
        harvest = Harvest.query

        # Search by query in title and abstract
        harvest = harvest.filter(or_(Harvest.title.contains(q),Harvest.abstract.contains(q)) )

        # Search by harvest url
        harvest = harvest.filter(Harvest.harvested_from == harvest_url)

        # Add pagination
        result = harvest.paginate(page, per_page, error_out=False)

        items_geojson = []

        # Post-process to get item_geojson
        if result.items:
            for i in result.items:
                items_geojson.append(i.item_geojson)
            result.items = items_geojson

            return {
                'result': marshal(result, page_of_items),
                'success': True,
                'message': {
                    'code': 200,
                    'description': 'Harvested items found'
                }
            }, 200
        else:
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'No harvested items found from this url'
                }
            }, 404

@ns.route('/harvest')
@api.response(400, 'Error harvesting')
@api.response(200, 'Harvested successfuly from remote catalogue.')
class HarvestCollection(Resource):
    @api.expect(p.harvest_args)
    def post(self):
        """
        Harvests records from a remote catalogue.
        """
        url = p.harvest_args.parse_args(request).get('url')
        harvester = p.harvest_args.parse_args(request).get('harvester')
        current_app.logger.info('Harvesting from: ' + url)
        try:
            total = harvest(url, harvester)
        except Exception as ex:
            current_app.logger.error('Error harvesting: ' + str(ex))
            return {
                'success': False,
                'message': {
                    'code': 400,
                    'description': 'Error harvesting ' + str(ex)
                }
            }, 400
        return {
            'success': True,
            'message': {
                'code': 200,
                'description': 'Harvested successfuly {0} datasets from {1} remote catalogue: {2}'.format(total, harvester, url)
            }
        }, 200

@ns.route('/draft/create_from_iso/')
class ItemCollection(Resource):
    @api.expect(p.iso_arg)
    @api.response(200, 'Draft successfully created.')
    @api.response(400, 'Draft creation failed')
    def post(self):
        """
        Creates a new item (draft) from iso(xml).
        """
        iso = p.iso_arg.parse_args(request).get('xml')

        md = MD_Metadata(etree.fromstring(iso))
        converted_data = convert_from_iso(md)

        try:
            actions.validate_input(converted_data)
            id = actions.create_draft(converted_data)
        except Exception as ex:
            current_app.logger.error(': ' + str(ex))
            return {
                'success': False,
                'message': {
                    'code': 400,
                    'description': 'Draft creation failed: ' + str(ex)
                }
            }, 400
        return {
            'success': True,
            'message': {
                'code': 200,
                'description': 'Draft successfully created.'
            }
        }, 200


@ns.route('/draft/create_from_harvest/<string:id>')
class ItemUnit(Resource):
    @api.response(404, 'Harvested item not found.')
    @api.response(400, 'Draft creation failed')
    @api.response(200, 'Draft successfully created.')
    def post(self, id):
        """
        Creates a new draft from an existing harvest item.
        """
        try:
            harvest = Harvest.query.filter(Harvest.id == id).one()
            actions.create_draft_from_item(harvest)
            actions.delete_harvested_item(harvest.id)
        except NoResultFound:
            current_app.logger.error('Harvested item not found.')
            return {
                'success': False,
                'message': {
                    'code': 404,
                    'description': 'Harvested item not found.'
                }
            }, 404
        except IntegrityError:
            current_app.logger.error('Draft for this harvested item already exists')
            return {
                'success': False,
                'message': {
                    'code': 400,
                    'description': 'Draft for this harvested item already exists.'
                }
            }, 400
        except Exception as ex:
            current_app.logger.error('Draft creation failed: ' + str(ex))
            return {
                'success': False,
                'message': {
                    'code': 400,
                    'description': 'Draft creation failed: ' + str(ex)
                }
            }, 400
        return {
            'success': True,
            'message': {
                'code': 200,
                'description': 'Draft successfully created.'
            }
        }, 200

@ns.route('/validate_schema')
@api.response(400, 'Invalid schema')
@api.response(200, 'Schema passed validation.')
class Validate(Resource):
    @ns.expect(item_geojson)
    def post(self):
        """
        Validates a json.
        """
        data = request.json
        try:
            actions.validate_input(data)
        except Exception as ex:
            current_app.logger.error('Error validating schema: ' + str(ex))
            return {
                'success': False,
                'message': {
                    'code': 400,
                    'description': 'Error validating schema: ' + str(ex)
                }
            }, 400

        return {
            'success': True,
            'message': {
                'code': 200,
                'description': 'Schema passed validation.'
            }
        }, 200
