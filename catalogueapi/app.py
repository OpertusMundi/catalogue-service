import logging.config

import os
from flask import Flask, Blueprint
from catalogueapi.api.items import ns as item_namespace
from catalogueapi.api.restx import api
from catalogueapi.database import db

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config.from_pyfile('config.py')
    if 'CONFIG_ENV' in os.environ:
        flask_app.config.from_envvar('CONFIG_ENV')

def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(item_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()

def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=app.config['FLASK_DEBUG'])


if __name__ == "__main__":
    main()