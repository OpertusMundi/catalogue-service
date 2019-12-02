# catalogue-api
====================


A simple catalogue api with functions create, update, delete, get all



config.ini file
-------

[DEFAULT]
 Flask settings

FLASK_SERVER_NAME = localhost:port
FLASK_DEBUG = true 	(set to false on production environments)

 Flask-Restplus settings

RESTPLUS_SWAGGER_UI_DOC_EXPANSION = list
RESTPLUS_VALIDATE = true
RESTPLUS_MASK_SWAGGER = false
RESTPLUS_ERROR_404_HELP = false

 SQLAlchemy settings

SQLALCHEMY_DATABASE_URI = postgresql://username:password@host:port/database
SQLALCHEMY_TRACK_MODIFICATIONS = false
