# file: main.py
import json
import requests
import logging
import service as svc
import request_handler as rh
from requests.exceptions import ConnectionError

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def search(args):
    genes = args['genes']
    response_format = 'json'

    token = args['_token']
    svc_url = svc.get_svc_base_url()

    try:
            response = rh.build_payload(svc_url, token, args)
            print json.dumps(response)
            print '---'
    except ValueError as e:
         error_msg = "ValueError Exception:" + e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)
    except requests.exceptions.HTTPError as e:
         error_msg = "HTTPError Exception:" + e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)
    except ConnectionError as e:
         error_msg = "ConnectionError Exception:" + e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)
    except Exception as e:
         error_msg = "GenericError Exception:" + e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)

def list(args):
     raise Exception('Not implemented yet')