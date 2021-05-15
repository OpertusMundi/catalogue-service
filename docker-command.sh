#!/bin/bash
set -u -e -o pipefail

[[ "${DEBUG:-False}" == "True" || "${XTRACE:-False}" == "True" ]] && set -x

#
# Check environment
#

python_version="$(python3 -c 'import platform; print(platform.python_version())' | cut -d '.' -f 1,2)" 
if [ "${python_version}" != "${PYTHON_VERSION}" ]; then
    echo "PYTHON_VERSION (${PYTHON_VERSION}) differs from version reported from python3 executable (${python_version})" 1>&2
    exit 1
fi

if [ -z "${SQLALCHEMY_DATABASE_URI}" ]; then
    echo "SQLALCHEMY_DATABASE_URI is not specified!" 1>&2
    exit 1
fi

database_server_pattern='^postgresql[:][/][/]([\w][\w\d-]*[:][^@]+)[@]\K([\w][\w\d-]*([.][\w][\w\d-]*)*)[:]([\d]{2,4})(?=[/])'
database_server=$(echo ${SQLALCHEMY_DATABASE_URI} | grep -Po -e "${database_server_pattern}" || echo -n)
if [ -z "${database_server}" ]; then
    echo "The database URL (SQLALCHEMY_DATABASE_URI) is malformed!" 1>&2 
    exit 1;
fi

if [ ! -f "${SECRET_KEY_FILE}" ]; then
    echo "SECRET_KEY_FILE does not exist!" 1>&2
    exit 1
fi

if [ ! -f "${LOGGING_FILE_CONFIG}" ]; then
    echo "LOGGING_FILE_CONFIG (configuration for Python logging) does not exist!" 1>&2
    exit 1
fi

logging_file_config=${LOGGING_FILE_CONFIG}
if [ -n "${LOGGING_ROOT_LEVEL}" ]; then
    logging_file_config="logging-$(echo ${HOSTNAME}| md5sum| head -c10).conf"
    sed -e "/^\[logger_root\]/,/^\[.*/ { s/^level=.*/level=${LOGGING_ROOT_LEVEL}/ }" ${LOGGING_FILE_CONFIG} \
        > ${logging_file_config}
fi

export FLASK_APP="catalogueapi"
export SECRET_KEY="$(cat ${SECRET_KEY_FILE})"

#
# Initialize database schema (if requested so)
#

wait-for-it -t '30' "${database_server}"

if [ "${DATABASE_INITIALIZE_SCHEMA:-False}" == "True" ]; then
    echo "Generating database schema..." 1>&2
    python -c 'import catalogueapi; catalogueapi.generate_db_schema()'
fi

#
# Start WSGI server
#

if [ "${FLASK_ENV}" == "development" ]; then
    # Run a development server
    LOGGING_FILE_CONFIG=${logging_file_config} exec /usr/local/bin/wsgi.py
else
    # Run a production server (Gunicorn)
    num_workers="4"
    server_port="5000"
    gunicorn_ssl_options=
    if [ -n "${TLS_CERTIFICATE}" ] && [ -n "${TLS_KEY}" ]; then
        gunicorn_ssl_options="--keyfile ${TLS_KEY} --certfile ${TLS_CERTIFICATE}"
        server_port="5443"
    fi
    exec gunicorn --log-config ${logging_file_config} --access-logfile - \
      --workers ${num_workers} \
      --bind "0.0.0.0:${server_port}" ${gunicorn_ssl_options} \
      'catalogueapi.app:create_app()'
fi
