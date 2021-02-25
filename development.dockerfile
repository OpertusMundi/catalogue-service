# vim: set syntax=dockerfile:

FROM python:3.8-slim-buster

ARG VERSION

ENV VERSION="${VERSION}"
ENV PYTHON_VERSION="3.8"

RUN apt-get update && apt-get install --yes \
        ca-certificates wait-for-it \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --uid 1000 --gecos '' --disabled-password flask

WORKDIR /home/flask

RUN chown --recursive flask:flask .

COPY --chown=flask requirements.txt ./

RUN python3 -m pip install --requirement requirements.txt

COPY --chown=flask . .

ENV FLASK_APP="catalogueapi" \
    FLASK_ENV="development" \
    LOGGING_FILE_CONFIG="./logging.conf" \
    SECRET_KEY_FILE="/var/local/catalogueapi/secret_key" \
    TLS_CERTIFICATE="" \
    TLS_KEY=""

COPY wsgi.py docker-command.sh /usr/local/bin/

RUN python3 -m pip install --editable .

USER flask
CMD ["/usr/local/bin/docker-command.sh"]

EXPOSE 5000
EXPOSE 5443
