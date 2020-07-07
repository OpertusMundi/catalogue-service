from flask_restx import reqparse

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('per_page', type=int, required=False,
                                  default=2, help='Results per page }')

search_arguments = reqparse.RequestParser()
search_arguments.add_argument('q', type=str, required=False, default="", help='Search query')
search_arguments.add_argument('bbox', type=str, required=False, default="", help='Bounding box')
search_arguments.add_argument('time', type=str, required=False, default="", help='Time extent')
search_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
search_arguments.add_argument('per_page', type=int, required=False,
                                  default=2, help='Results per page }')

id_args = reqparse.RequestParser()
id_args.add_argument('id', type=str, required=True, action='split', help='Ids of the items')