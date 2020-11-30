# catalogue-service

A catalogue service with CRUD operations.

## Installation

```
pip install -r requirements.txt
python setup.py install
```

run with: `python app.py`

## Configuration

Use the `config.py` file:

```
SERVER_NAME = 'localhost:port'
FLASK_DEBUG = True 	(set to False on production environments)

SWAGGER_UI_DOC_EXPANSION = list
RESTX_VALIDATE = True
RESTX_MASK_SWAGGER = False
ERROR_404_HELP = False

SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@host:port/database'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```
