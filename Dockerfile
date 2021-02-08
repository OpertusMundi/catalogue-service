FROM python:3.8-slim-buster

RUN apt-get update && apt-get install --yes \
        ca-certificates wait-for-it \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --uid 1000 --gecos '' --disabled-password flask

WORKDIR /home/flask

RUN chown --recursive flask:flask .

COPY --chown=flask \
    requirements.txt \
    requirements-production.txt \
    ./

RUN python3 -m pip install \
    --requirement requirements.txt \
    --requirement requirements-production.txt

COPY --chown=flask . .

ENV FLASK_APP="catalogueapi" \
    TLS_CERTIFICATE="" \
    TLS_KEY=""

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN python3 -m pip install --editable .

USER flask
CMD ["/usr/local/bin/entrypoint.sh"]

EXPOSE 5000
EXPOSE 5443
