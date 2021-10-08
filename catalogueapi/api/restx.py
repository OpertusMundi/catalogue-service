import os
from distutils.util import strtobool
from flask import current_app
from flask_restx import Api
import sqlalchemy.orm.exc

from ..logging import exception_as_rfc5424_structured_data 

api = Api(version='1.0', title='Catalogue service',
          description='A catalogue service implemented with a Flask RESTX powered API')

debug = strtobool(os.environ.get('FLASK_DEBUG', 'False'))

@api.errorhandler
def default_error_handler(e):
    current_app.logger.error('An unhandled exception occurred: %s', e, 
        extra=exception_as_rfc5424_structured_data(e))
    if not debug:
        return {'message': 'An unexpected error occurred'}, 500


@api.errorhandler(sqlalchemy.orm.exc.NoResultFound)
def database_not_found_error_handler(e):
    current_app.logger.warning("A database item was expected but was not found: %s", e)
    return {'message': 'A result was required but none was found.'}, 404
