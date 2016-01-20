# file: main.py
import json
import requests
import logging
import service as svc
import request_handler as rh
from requests.exceptions import ConnectionError
import exception

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def search(args):

    token = args['_token']
    svc_url = svc.get_svc_base_url()

    try:
         response = rh.build_payload(svc_url, token, args)
         print json.dumps(response)
         print '---'
    except ValueError as e:
         error_msg = "Value Error:" + e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)
    except requests.exceptions.HTTPError as e:
         error_msg = "HTTP Error:" + e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)
    except ConnectionError as e:
         error_msg = "Connection Error:" + e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)
    except exception.NotFound as e:
         error_msg = e.message
         log.error(error_msg, exc_info=True)
         response = "{}"
         print json.loads(response)
         print '---'
    except exception.InvalidParameter as e:
         error_msg = e.message
         log.error(error_msg, exc_info=True)
         raise exception.InvalidParameter(error_msg)
    except exception.EmptyResponse as e:
         error_msg = e.message
         log.error(error_msg, exc_info=True)
         raise exception.EmptyResponse(error_msg)
    except Exception as e:
         error_msg = e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)

def list(args):
     raise Exception('Not implemented yet')
