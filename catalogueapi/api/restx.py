import logging
import traceback
import configparser
from flask_restx import Api
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

api = Api(version='1.0', title='A simple catalogue api',
          description='A simple implementation of a Flask RESTX powered API')


config = configparser.ConfigParser()
config.read('config.ini')

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)
    
    if not config.getboolean('DEFAULT','FLASK_DEBUG'):
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404