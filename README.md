# catalogue-service

A catalogue service with CRUD operations.

## 1. Install

Needs Python >= `3.8`.

Install requirements and package:

    pip install -r requirements.txt
    python setup.py install


## 2. Configure

The application is configured using environment variables:
  
 * `SECRET_KEY` (optional): a randomly-generated secret used for encryption
 * `SQLALCHEMY_DATABASE_URI`: the SQLAlchemy connection URL for PostGIS (>=`3.0`) backend (`postgresql://username:password@host:port/database`)
 * `SQLALCHEMY_TRACK_MODIFICATIONS`: A `True/False` flag
 * `SERVER_NAME` (optional): the server name (`host:port`) under which the service is accessed.
 * `SWAGGER_UI_DOC_EXPANSION`: one of `none`, `list` or `full`
 * `RESTX_VALIDATE`: a `True/False` flag
 * `RESTX_MASK_SWAGGER`: a `True/False` flag
 * `ERROR_404_HELP`: a `True/False` flag
 * `FLASK_DEBUG`: a `True/False` flag (should be `False` in a production environment!)

For convenience, these variables can be kept in an enviroment-like file, say `config-development.py` or `config-testing.py`. 
Look at the example at `config-development.py.example`.  

## 3. Run

Run a development server (environment variables must be set in current shell):

    ./wsgi.py
 
If environment variables are kept in a seperate file, say `development.env`, run by pointing to that file:

    env FILE_CONFIG=config-development.py ./wsgi.py

## 4. Run with Docker

To run with Docker we must prepare a `docker-compose` recipe.

Copy `.env.example` into `.env`. Edit as needed.

The additional environment variables here (i.e. not described in section [2](#2-configure)):

  * `FLASK_ENV`: One of `production` or `development`
  * `VERSION`: The semantic version of the application (used to tag the Docker image)

Copy `docker-compose.yml.example` into `docker-compose.yml`. Edit as needed. You will at least need to configure the network (inside `docker-compose.yml`) to attach to. 

For example, you can create a private network named `opertusmundi_network`:

    docker network create --attachable opertusmundi_network

Build the image:

    docker-compose build
   
Run:

    docker-compose up -d

