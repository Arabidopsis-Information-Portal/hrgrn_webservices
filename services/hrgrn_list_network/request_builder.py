# file: request_builder.py

import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def build_param_map(args):
    params = {}

    for key, value in args.iteritems():
        if (key == 'locus'):
            params['foreignID'] = value
        else:
            params[key] = value

    params['format'] = 'json'

    return params
