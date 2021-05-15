#!/usr/bin/env python
import os
import os.path
import catalogueapi

if __name__ == '__main__':
    if 'FILE_CONFIG' in os.environ:
        catalogueapi.generate_db_schema(os.path.realpath(os.environ.get('FILE_CONFIG')))
    else:
        catalogueapi.generate_db_schema()
