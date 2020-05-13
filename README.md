# catalogue-api

A simple catalogue API with functions `create`, `update`, `delete` and `get all`.

## Installation

```
pip install -r requirements.txt
python setup.py develop
```

run with: `python app.py`

## Configuration

Use the `config.ini` file:

```
[DEFAULT]
;Flask settings
FLASK_SERVER_NAME = localhost:port
FLASK_DEBUG = true 	(set to false on production environments)

;Flask-RESTX settings
RESTX_SWAGGER_UI_DOC_EXPANSION = list
RESTX_VALIDATE = true
RESTX_MASK_SWAGGER = false
RESTX_ERROR_404_HELP = false

;SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = postgresql://username:password@host:port/database
SQLALCHEMY_TRACK_MODIFICATIONS = false
```
