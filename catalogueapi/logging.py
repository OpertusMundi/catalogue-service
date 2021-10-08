import os
import sys
import traceback
import logging
from itertools import chain

APP_NAME = os.environ.get('FLASK_APP')

#
# Utilities
#

def exception_as_rfc5424_structured_data(ex):
    
    tb = traceback.format_exception(*sys.exc_info());
    
    return {
        'structured_data': {
            'mdc': {
                'exception-message': str(ex),
                'exception': '|'.join(chain.from_iterable((s.splitlines() for s in tb[1:]))),
            }
        }
    };


#
# Context filters for loggers
#

class Rfc5424MdcContextFilter(logging.Filter):
    """A filter injecting diagnostic context suitable for RFC5424 messages"""
    
    def filter(self, record):
        record.msgid = APP_NAME
        if not hasattr(record, 'structured_data'):
            record.structured_data = {'mdc': {}}
        mdc = record.structured_data.get('mdc') 
        if mdc is None:
            mdc = record.structured_data['mdc'] = {}
        mdc.update({
            'logger': record.name,
            'thread': record.threadName
        })
        return True;

