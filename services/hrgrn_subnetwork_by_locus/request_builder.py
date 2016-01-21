# file: request_builder.py
import logging

import exception
import gene_info_service as gi
import service as svc


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

    # add default parameters
    params['hasParams'] = 'T'
    params['format'] = 'json'
    
    # extract gene nodes
    validateParameters(args)
    genes = args['genes']
    
    try:
            _url, _namespace = args['_url'], args['_namespace']
            log.debug("Url:" + str(_url) + ";" + " Namespace: " + str(_namespace))
    except:
        log.warn("No _url/_namespace parameters in the request. Will use default service values." )
        
    list_gene_nodes = gi.get_nodes_by_genes(svc.gene_svc_url(url=_url, namespace=_namespace), \
        token, genes)
    
    hasValue('target_genes', list_gene_nodes, "No genes have been submitted!")
    
    nodes = parse_gene_node_parameters(list_gene_nodes)
    hasValue('target_nodes', nodes, "No genes have been submitted!")
    params['nodes'] = nodes

   # extract other parameters
    for key, value in args.iteritems():
        if not (key == 'locus'):
            if ((key in edge_type_params_map.keys()) and value == 'true'):
                _boolean_key = edge_type_params_map[key]
                params[_boolean_key] = 'T'
                log.debug("Edge Type Key:" + _boolean_key + ";Edge Type Value:" + value)

            if key in param_value_map.keys():
                _key = param_value_map[key]
                params[_key] = value
                log.debug("Parameter Key:" + _boolean_key + ";Parameter Value:" + value)

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
    
def hasParam(params, param_key, error_msg):
    
    if not error_msg:
        error_msg = "No Parameter " + str(param_key) + " is present"
   
    log.info("Param Key:" + param_key)
    
    if param_key in params.keys():
            return True
    else:
            raise exception.InvalidParameter(error_msg)
        
def hasValue(_key, _value, error_msg):
    
    if not error_msg:
        error_msg = "No Value for " + str(_key) + " is present"
       
    if _value:
        return True
    else:
            raise exception.InvalidParameter(error_msg)  
    
    
def validateParameters(params):
    
    # validate gene input parameters
    _key_genes = 'genes'
    error_msg = "No genes have been submitted!"
    
    log.info("Testing params")
    log.info(params)
        
    try:
        hasParam(params, _key_genes, error_msg)
    except Exception as e:
        raise exception.InvalidParameter(error_msg)
 
    _value =params[_key_genes]
    
    hasValue(_key_genes, _value, "Empty genes parameter value have been submitted!")
       
