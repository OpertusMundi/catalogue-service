from flask_restx import reqparse

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
draft_search_args.add_argument('status', type=str, required=False, default="", help='Item status')
draft_search_args.add_argument('page', type=int, required=False, default=1, help='Page number')
draft_search_args.add_argument('per_page', type=int, required=False,
                                  default=5, help='Results per page }')

id_args = reqparse.RequestParser()
id_args.add_argument('id', type=str, required=True, action='split', help='Ids of the items')

update_status_args = reqparse.RequestParser()
update_status_args.add_argument('id', type=str, required=False, default="", help='Item/draft id')
update_status_args.add_argument('status', type=str, required=False, default="", help='Status to be updated (review - accepted - published)')