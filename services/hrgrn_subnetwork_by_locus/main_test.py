# file: main_test.py
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
import request_builder as rb
import request_handler as rh
from requests.exceptions import ConnectionError

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

TOKEN="e94cca90bdfcfee77f66d6b821e6265e"

def search(arg):
    genes = arg['genes']
    response_format = 'json'

    #svc_url = rb.build_svc_url(genes)
    svc_url = svc.get_svc_base_url_temp()

    try:
            response = rh.build_payload(svc_url, TOKEN, arg)
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

def main():
    """test logic for when running this module as the primary one!"""
    args = {'genes': 'AT2G38470,AT3G55734,AT2G39885,AT3G26810', 'pathalg':'allSimplePaths', 'steps':'2','proteinModification':'validated,predicted', 'ppiInteraction':'validated,predicted', 'cpi':'validated,predicted','geneExpressionRegulation':'validated,predicted', 'srnaRegulation':'validated,predicted', 'transportedMolecule':'validated,predicted', 'composition':'validated,predicted', 'coexpressedGenePair':'validated,predicted', 'coexpValueCutoff':'0.8', 'cutoffNodeRelationships':'100'}
    search(args)
    param_map = rb.build_param_map(args, TOKEN)
    log.info("Param Map:")
    log.info(param_map)


if __name__ == '__main__':
    main()
