# file: main_test.py
import json
import requests
import logging
import service as svc
import request_builder as rb
import request_handler as rh
import main as driver
from requests.exceptions import ConnectionError


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

TOKEN="8d7cf82b6c77503671bc5f6a2492bda3"

def search(arg):
    genes = arg['locus']
    response_format = 'json'

    #svc_url = rb.build_svc_url(genes)
    svc_url = svc.get_svc_base_url()

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
    args = {'locus': 'AT2G38470', 'pathalg':'allSimplePaths', 'steps':'2', 'showValidatedEdge': 'true', 'showPredictedEdge':'true', 'proteinModification':'true', 'ppiInteraction':'true', 'showppiInteractionPredicted': 'true', 'cpi':'true','geneExpressionRegulation':'true', 'srnaRegulation':'true', 'showsrnaRegulationPredicted': 'true', 'transportedMolecule':'true', 'composition':'true', 'coexpressedGenePair':'true', 'coexpValueCutoff':'0.8', 'cutoffNodeRelationships':'100', '_url': 'https://api.araport.org/community/v0.3', '_namespace': 'hrgrn'}
    search(args)
    param_map = rb.build_param_map(args, TOKEN)
    log.info("Param Map:")
    log.info(param_map)


if __name__ == '__main__':
    main()
