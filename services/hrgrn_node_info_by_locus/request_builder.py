# file: request_builder.py

import logging
import exception

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def build_param_map(args):
    params = {}

    validateParameters(args)

    for key, value in args.iteritems():
        if (key == 'locus'):
            params['foreignID'] = value
        else:
            params[key] = value

    params['format'] = 'json'

    return params

def validateParameters(params):
    _key_geneID = 'locus'

    try:
        if not _key_geneID in params.keys():
            raise exception.InvalidParameter(exception.no_geneID_parameter_error_msg)
    except Exception as e:
        raise exception.InvalidParameter(exception.no_geneID_parameter_error_msg)

def getGeneID(params):

    # locus
    _key_geneID = 'locus'

    try:
        if _key_geneID in params.keys():
            geneID = params[_key_geneID]
            return geneID
        else:
            raise exception.InvalidParameter(exception.no_geneID_parameter_error_msg)
    except Exception as e:
        raise exception.InvalidParameter(exception.no_geneID_parameter_error_msg)
