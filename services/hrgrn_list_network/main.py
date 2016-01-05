# file: main.py
import json
import requests
import logging
import timer as timer
from requests.exceptions import ConnectionError
from requests import Session
import service as svc
import request_handler as rh

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def list(args):
    session = Session()
    svc_url = svc.get_svc_base_url()

    params = {'listall': 'T', 'format':'json'}

    try:
        with timer.Timer() as t:
            log.info("Service URL:" + svc_url)
            #response = rh.build_payload(svc_url, params, session)
            response = rh.handle_request(svc_url, params)
            log.debug(response.text)
            #if (response):
                #return 'application/json' , json.dumps(json.loads(response.text))
            #else:
                #raise Exception("Response cannot be null!")
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
    finally:
            log.info('Request took %.03f sec.' % t.interval)

    return 'application/json' , json.dumps(json.loads(response.text))
