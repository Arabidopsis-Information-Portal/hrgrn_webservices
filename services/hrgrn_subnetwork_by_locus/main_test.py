# file: main_test.py
import json
import logging

import exception
import main as driver
import request_builder as rb
import request_handler as rh
import requests
from requests.exceptions import ConnectionError
import service as svc


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

TOKEN = "add494c5da31e4e678dc2d29a32f97b4"

def search(args):
    genes = args['genes']
    response_format = 'json'

    token = TOKEN
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

def main():
    """test logic for when running this module as the primary one!"""

    # # pass the namespace you test again (your dev namespace or production)
    test_namespace = 'ibelyaev-dev'

    # valid arguments test case
    args = {'genes': 'AT2G38470,AT3G55734,AT2G39885', 'pathalg':'allSimplePaths', 'steps':'2', 'showValidatedEdge': 'true', 'showPredictedEdge':'true', 'proteinModification':'true', 'showproteinModificationPredicted': 'false', 'ppiInteraction':'true', 'showppiInteractionPredicted': 'false', 'cpi':'true', 'showcpiPredicted':'false', 'geneExpressionRegulation':'true', 'showgeneExpressionRegulationPredicted':'false', 'srnaRegulation':'true', 'showsrnaRegulationPredicted': 'true', 'transportedMolecule':'true', 'showtransportedMoleculePredicted':'false', 'composition':'true', 'showcompositionPredicted':'true' , 'coexpressedGenePair':'false', 'showcoexpressedGenePairPredicted':'true', 'chemReaction':'true', 'showchemReactionPredicted':'false', 'coexpValueCutoff':'0.8', 'cutoffNodeRelationships':'100', '_url': 'https://api.araport.org/community/v0.3', '_namespace': test_namespace}
    
    # inavalid arguments test case - should return empty JSON array
    #args = {'genes': 'Y,X,AT2G39885', 'pathalg':'allSimplePaths', 'steps':'2', 'showValidatedEdge': 'true', 'showPredictedEdge':'true', 'proteinModification':'true', 'showproteinModificationPredicted': 'false', 'ppiInteraction':'true', 'showppiInteractionPredicted': 'false', 'cpi':'true', 'showcpiPredicted':'false', 'geneExpressionRegulation':'true', 'showgeneExpressionRegulationPredicted':'false', 'srnaRegulation':'true', 'showsrnaRegulationPredicted': 'true', 'transportedMolecule':'true', 'showtransportedMoleculePredicted':'false', 'composition':'true', 'showcompositionPredicted':'true' ,'coexpressedGenePair':'false','showcoexpressedGenePairPredicted':'true', 'chemReaction':'true', 'showchemReactionPredicted':'false', 'coexpValueCutoff':'0.8', 'cutoffNodeRelationships':'100', '_url': 'https://api.araport.org/community/v0.3', '_namespace': test_namespace}

    search(args)


if __name__ == '__main__':
    main()
