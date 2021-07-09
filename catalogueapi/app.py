import os
import os.path
from flask import Flask, Blueprint

def create_app(config_file=None):
    
    from .api.items import ns as item_namespace
    from .api.restx import api
    from .database import db
    
    app = Flask(__name__)
    
    # Configure app

    if config_file:
        # Configure from Python environment-like file
        app.config.from_pyfile(config_file)
    else:
        # Configure (directly) from environment
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
        app.config['SERVER_NAME'] = os.environ.get('SERVER_NAME') or None 
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False) 
        app.config['SWAGGER_UI_DOC_EXPANSION'] = os.environ.get("SWAGGER_UI_DOC_EXPANSION", 'list') 
        app.config['RESTX_VALIDATE'] = os.environ.get("RESTX_VALIDATE", True) 
        app.config['RESTX_MASK_SWAGGER'] = os.environ.get("RESTX_MASK_SWAGGER", False) 
        app.config['ERROR_404_HELP'] = os.environ.get("ERROR_404_HELP", False)
        app.config['FLASK_DEBUG'] = os.environ.get("FLASK_DEBUG", False)
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}
       
    # Register blueprints

    api_blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(api_blueprint)
    api.add_namespace(item_namespace)
    app.register_blueprint(api_blueprint)
    
    # Register SQLAlchemy extension with this Flask application

    db.init_app(app)

    return app

