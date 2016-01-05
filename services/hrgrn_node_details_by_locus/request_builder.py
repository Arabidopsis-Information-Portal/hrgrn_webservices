# file: request_builder.py
import json
import logging
import service as svc
import gene_info_service as gi

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
    geneID = args['locus']
    gene_params = { 'locus':geneID }
    _url, _namespace = args['_url'], args['_namespace']
    gene_nodeID = gi.get_node_by_gene_id(svc.gene_svc_url(url=_url, namespace=_namespace), \
        token, gene_params)
    log.info("Target Node:" + gene_nodeID)
    if (gene_nodeID):
        params['grnID'] = gene_nodeID

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
