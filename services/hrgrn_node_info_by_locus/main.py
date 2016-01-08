# file: main.py
import json
import requests
import logging
import timer as timer
from requests.exceptions import ConnectionError
from requests import Session
import service as svc
import request_handler as rh
import exception

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Invoke HRGRN web services given a gene ID and output format parameters
# See http://plantgrn.noble.org/hrgrn/
# Example URI: http://plantgrn.noble.org/hrgrn/nodes?foreignID=AT3G46810&format=json

def search(arg):
    locus = arg['locus']
    response_format = 'json'

    session = Session()
    svc_url = svc.get_svc_base_url()

    try:
        response = rh.build_payload(svc_url, arg, session)
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
         raise exception.NotFound(error_msg)
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
