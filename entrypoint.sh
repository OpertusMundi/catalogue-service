#!/bin/sh
#set -x
set -e

export FLASK_APP="catalogueapi"

# Wait for database to startup
wait-for-it -t 30 "db:5432"

# Initialize database
flask init-db

# Configure and start WSGI server

if [ "${FLASK_ENV}" == "development" ]; then
    # Run a development server
    exec /home/flask/catalogueapi/app.py
fi

num_workers="4"
server_port="5000"
gunicorn_ssl_options=
if [ -n "${TLS_CERTIFICATE}" ] && [ -n "${TLS_KEY}" ]; then
    gunicorn_ssl_options="--keyfile ${TLS_KEY} --certfile ${TLS_CERTIFICATE}"
    server_port="5443"
fi

exec gunicorn - \
  --workers ${num_workers} \
  --bind "0.0.0.0:${server_port}" ${gunicorn_ssl_options} \
  catalogueapi.app:app
