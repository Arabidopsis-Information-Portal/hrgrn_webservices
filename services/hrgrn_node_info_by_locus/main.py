# file: main.py
import json
import requests
import logging
import timer as timer
from requests.exceptions import ConnectionError
import service as svc
import request_handler as rh

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Invoke HRGRN web services given a gene ID and output format parameters
# See http://plantgrn.noble.org/hrgrn/
# Example URI: http://plantgrn.noble.org/hrgrn/nodes?foreignID=AT3G46810&format=json

# Response: [
#    {data: {id:'np13163',label:'4CL.1',type:'Protein',tftr:'',tips:'4CL.1; 4CL1; AT4CL1, AT1G51680, ID=np13163, Protein',locus:'AT1G51680',shape:'ellipse',background_color:'#FCFCFC',border_color:'#585858',color:'#000000'} }
# ] which is invalid JSON

def search(arg):
    locus = arg['locus']
    response_format = 'json'

    svc_url = svc.get_svc_base_url()

    try:
        response = rh.build_payload(svc_url, arg)
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
     #getAllGeneNodes(args)
     raise Exception('Not implemented yet')

def getAllGeneNodes(args):
    svc_url = svc.get_svc_base_url()

    params = {'listall': 'T'}

    try:
        with timer.Timer() as t:
            log.info("Service URL:" + svc_url)
            response = rh.build_payload(svc_url, params)
            log.info(response)
            if (response):
                print json.dumps(response)
                print '---'
            else:
                raise Exception("Response cannot be null!")
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
