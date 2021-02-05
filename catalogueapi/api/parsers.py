from flask_restx import reqparse, inputs

pagination_args = reqparse.RequestParser()
pagination_args.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_args.add_argument('per_page', type=int, required=False,
                                  default=2, help='Results per page }')

pub_search_args = reqparse.RequestParser()
pub_search_args.add_argument('publisher_id', type=str, required=False, default="", help='Publisher id')
pub_search_args.add_argument('q', type=str, required=False, default="", help='Search query')
pub_search_args.add_argument('bbox', type=str, required=False, default="", help='Bounding box')
pub_search_args.add_argument('time', type=str, required=False, default="", help='Time extent')
pub_search_args.add_argument('page', type=int, required=False, default=1, help='Page number')
pub_search_args.add_argument('per_page', type=int, required=False,
                                  default=5, help='Results per page }')

draft_search_args = reqparse.RequestParser()
draft_search_args.add_argument('publisher_id', type=str, required=False, default="", help='Publisher id')
draft_search_args.add_argument('status', type=str, required=False, default="", action='split', help='Item status')
draft_search_args.add_argument('page', type=int, required=False, default=1, help='Page number')
draft_search_args.add_argument('per_page', type=int, required=False,
                                  default=5, help='Results per page }')

history_search_args = reqparse.RequestParser()
history_search_args.add_argument('item_id', type=str, required=False, default="", help='Item id')
history_search_args.add_argument('publisher_id', type=str, required=False, default="", help='Publisher id')
history_search_args.add_argument('deleted', type=inputs.boolean, required=False, default=False, help='Deleted status')
history_search_args.add_argument('page', type=int, required=False, default=1, help='Page number')
history_search_args.add_argument('per_page', type=int, required=False,
                                  default=5, help='Results per page }')

history_get_args = reqparse.RequestParser()
history_get_args.add_argument('id', type=str, required=True, default="", help='Item id')
history_get_args.add_argument('version', type=str, required=True, default="", help='Item version')

id_args = reqparse.RequestParser()
id_args.add_argument('id', type=str, required=True, action='split', help='Ids of the items')

update_status_args = reqparse.RequestParser()
update_status_args.add_argument('id', type=str, required=True, default="", help='Item/draft id')
update_status_args.add_argument('status', type=str, required=True, default="", help='Status to be updated (review - accepted - published)')

harvest_args = reqparse.RequestParser()
harvest_args.add_argument('url', type=inputs.URL(schemes=['http', 'https'], local=True, port=True, ip=True), required=True, help='Harvest url')
harvest_args.add_argument('harvester', type=str, required=True, default="op-catalogue", help='Target catalogue type (op-catalogue/ckan)')