# file: request_builder.py

import json
import requests
import re
import gzip
import StringIO
import zlib
import urllib2
import demjson
import logging
import service as svc

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def build_param_map(args):
    params = {}

    for key, value in args.iteritems():
        if (key == 'geneID'):
            params['foreignID'] = value
        else:
            params[key] = value

    params['format'] = 'json'

    return params
