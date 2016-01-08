# file: request_builder.py
import json
import logging
import service as svc
import gene_info_service as gi
import exception

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def parse_gene_node_parameters(params):
    separator = ";"
    result = str(separator.join(params))
    return result

edge_type_params_map = {
  'proteinModification' : 'MODIFY_validated',
  'showproteinModificationPredicted' : 'MODIFY_predicted',
  'ppiInteraction' : 'PPI_validated',
  'showppiInteractionPredicted' : 'PPI_predicted',
  'cpi' : 'CPI_validated',
  'showcpiPredicted' : 'CPI_predicted',
  'geneExpressionRegulation' : 'GENEEXPREGU_validated',
  'showgeneExpressionRegulationPredicted' : 'GENEEXPREGU_predicted',
  'srnaRegulation' : 'SRNAREGU_validated',
  'showsrnaRegulationPredicted' : 'SRNAREGU_predicted',
  'transportedMolecule' : 'MOLTRANSPORT_validated',
  'showtransportedMoleculePredicted' : 'MOLTRANSPORT_predicted',
  'composition' : 'COMPOSITION_validated',
  'showcompositionPredicted' : 'COMPOSITION_predicted',
  'coexpressedGenePair' : 'COEXP_validated',
  'showcoexpressedGenePairPredicted' : 'COEXP_predicted',
  'chemReaction' : 'CHEMREACTION_validated',
  'showchemReactionPredicted' : 'CHEMREACTION_predicted'
  }

param_value_map = {
'pathalg' : 'pathalg',
'steps' : 'steps',
'coexpValueCutoff' : 'COEXP_value',
'cutoffNodeRelationships' : 'cutoffHubRels'
}

def build_param_map(args, token):
    params = {}

    params['hasParams']='T'
    # extract gene nodes
    genes = args['genes']
    _url, _namespace = args['_url'], args['_namespace']
    list_gene_nodes = gi.get_nodes_by_genes(svc.gene_svc_url(url=_url, namespace=_namespace), \
        token, genes)

    if (list_gene_nodes) and len(list_gene_nodes)==2:
        params['node1'] = list_gene_nodes[0]
        params['node2'] = list_gene_nodes[1]

        log.info("Node1:" +str(list_gene_nodes[0]))
        log.info("Node2:" +str(list_gene_nodes[1]))

    else:
        raise Exception("Only two genes can be submitted!")

   #extract other parameters
    for key, value in args.iteritems():
         if not (key == 'locus'):
             if ((key in edge_type_params_map.keys()) and value=='true'):
                 _boolean_key = edge_type_params_map[key]
                 params[_boolean_key] = 'T'
                 log.debug("Edge Type Key:" + _boolean_key + ";Edge Type Value:" + value)

             if key in param_value_map.keys():
                 _key = param_value_map[key]
                 params[_key] = value
                 log.debug("Parameter Key:" + _boolean_key + ";Parameter Value:" + value)

    params['format'] = 'json'


    return params

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
