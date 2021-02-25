#!/usr/bin/env python
import os
import os.path
import logging
import logging.config

# Configure logging before loading the application module
# see https://flask.palletsprojects.com/en/1.1.x/logging/#basic-configuration

#logging.basicConfig(level=logging.INFO);
logging.config.fileConfig(os.getenv('LOGGING_FILE_CONFIG', './logging.conf'));

from catalogueapi.app import create_app

if __name__ == '__main__':
    
    # Create app
    if 'FILE_CONFIG' in os.environ:
        app = create_app(os.path.realpath(os.environ['FILE_CONFIG']))
    else:
        app = create_app()
    
    # Configure server TLS
    ssl_context = None
    port = 5000
    tls_cert = os.environ.get('TLS_CERTIFICATE');
    tls_key = os.environ.get('TLS_KEY');
    if tls_cert and tls_key:
        ssl_context = (tls_cert, tls_key);
        port = 5443;
    
    # Run development server
    app.run(host="0.0.0.0", port=port, ssl_context=ssl_context);
