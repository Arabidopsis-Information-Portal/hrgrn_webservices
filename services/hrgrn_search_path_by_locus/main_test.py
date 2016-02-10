# file: main_test.py
import json
import requests
import logging
import service as svc
import request_builder as rb
import request_handler as rh
import main as driver
from requests.exceptions import ConnectionError
import exception


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

TOKEN="e0e9ab1c63dc118fa1278ec11b5d9bd0"

def search(args):
    genes = args['genes']
    response_format = 'json'

    #svc_url = rb.build_svc_url(genes)
    svc_url = svc.get_svc_base_url()

    token = TOKEN

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

    test_namespace = 'ibelyaev-dev'

    args = {'genes': 'AT2G38470,AT3G55734', 'pathalg':'allSimplePaths', 'steps':'2', 'showValidatedEdge': 'true', 'showPredictedEdge':'true', 'proteinModification':'true', 'showproteinModificationPredicted': 'false', 'ppiInteraction':'true', 'showppiInteractionPredicted': 'false', 'cpi':'true', 'showcpiPredicted':'false', 'geneExpressionRegulation':'true', 'showgeneExpressionRegulationPredicted':'false', 'srnaRegulation':'true', 'showsrnaRegulationPredicted': 'true', 'transportedMolecule':'true', 'showtransportedMoleculePredicted':'false', 'composition':'true', 'showcompositionPredicted':'true' ,'coexpressedGenePair':'false','showcoexpressedGenePairPredicted':'true', 'chemReaction':'true', 'showchemReactionPredicted':'false', 'coexpValueCutoff':'0.8', 'cutoffNodeRelationships':'100', '_url': 'https://api.araport.org/community/v0.3', '_namespace': test_namespace}
    #args = {'genes': 'AT2G38470,Y', 'pathalg':'allSimplePaths', 'steps':'2', 'showValidatedEdge': 'true', 'showPredictedEdge':'true', 'proteinModification':'true', 'showproteinModificationPredicted': 'false', 'ppiInteraction':'true', 'showppiInteractionPredicted': 'false', 'cpi':'true', 'showcpiPredicted':'false', 'geneExpressionRegulation':'true', 'showgeneExpressionRegulationPredicted':'false', 'srnaRegulation':'true', 'showsrnaRegulationPredicted': 'true', 'transportedMolecule':'true', 'showtransportedMoleculePredicted':'false', 'composition':'true', 'showcompositionPredicted':'true' ,'coexpressedGenePair':'false','showcoexpressedGenePairPredicted':'true', 'chemReaction':'true', 'showchemReactionPredicted':'false', 'coexpValueCutoff':'0.8', 'cutoffNodeRelationships':'100', '_url': 'https://api.araport.org/community/v0.3', '_namespace': test_namespace}

    search(args)


if __name__ == '__main__':
    main()
