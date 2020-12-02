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
    # initialize config option from file
    flask_app.config.from_pyfile('config.py')
    # replace with environmental values if existing
    flask_app.config['SERVER_NAME'] = os.environ.get("SERVER_NAME", flask_app.config['SERVER_NAME']) 
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI", flask_app.config['SQLALCHEMY_DATABASE_URI'])
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS']) 
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = os.environ.get("SWAGGER_UI_DOC_EXPANSION", flask_app.config['SWAGGER_UI_DOC_EXPANSION']) 
    flask_app.config['RESTX_VALIDATE'] = os.environ.get("RESTX_VALIDATE", flask_app.config['RESTX_VALIDATE']) 
    flask_app.config['RESTX_MASK_SWAGGER'] = os.environ.get("RESTX_MASK_SWAGGER", flask_app.config['RESTX_MASK_SWAGGER']) 
    flask_app.config['ERROR_404_HELP'] = os.environ.get("ERROR_404_HELP", flask_app.config['ERROR_404_HELP']) 
    

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