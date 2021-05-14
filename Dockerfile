FROM python:3.8-slim-buster

ARG VERSION

RUN apt-get update && apt-get install --yes ca-certificates wait-for-it \
    && rm -rf /var/lib/apt/lists/*

ENV VERSION="${VERSION}"
ENV PYTHON_VERSION="3.8"

RUN addgroup flask && \
    adduser --home /var/local/catalogueapi --disabled-login --ingroup flask --gecos '' flask

RUN pip3 install --upgrade pip

RUN mkdir /usr/local/catalogueapi

WORKDIR /usr/local/catalogueapi

COPY setup.py requirements.txt requirements-production.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt -r requirements-production.txt

COPY catalogueapi ./catalogueapi
RUN python setup.py install && python setup.py clean -a

COPY docker-command.sh wsgi.py /usr/local/bin/
RUN chmod a+x /usr/local/bin/docker-command.sh /usr/local/bin/wsgi.py

WORKDIR /var/local/catalogueapi

RUN mkdir ./logs && chown flask:flask ./logs
COPY --chown=flask logging.conf .

ENV FLASK_ENV="production" \
    FLASK_DEBUG="false" \
    LOGGING_FILE_CONFIG="./logging.conf" \
    LOGGING_ROOT_LEVEL="" \
    INSTANCE_PATH="/var/local/catalogueapi/data/" \
    SECRET_KEY_FILE="/var/local/catalogueapi/secret_key" \
    TLS_CERTIFICATE="" \
    TLS_KEY="" \
    SERVER_NAME=""

USER flask
CMD ["/usr/local/bin/docker-command.sh"]

EXPOSE 5000
EXPOSE 5443
