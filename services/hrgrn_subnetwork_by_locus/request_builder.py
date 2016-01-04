# file: request_builder.py
import logging
import service as svc
import gene_info_service as gi

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def get_svc_suffix_url():
    svc_suffix = '&steps=2&pathalg=allSimplePaths&COMPOSITION_validated=T&COMPOSITION_predicted=T&MODIFY_validated=T&PPI_validated=T&CPI_validated=T&GENEEXPREGU_validated=T&SRNAREGU_validated=T&SRNAREGU_predicted=T&MOLTRANSPORT_validated=T&CHEMREACTION_validated=T&COEXP_predicted=T&COEXP_value=0.8&cutoffHubRels=100&format=json'
    return svc_suffix

def build_parameters(params):
    separator = ";"
    result = 'nodes=' + separator.join(params.split(','))
    return result

def build_query_url(params):
    query_url = str(build_parameters(params)) + str(get_svc_suffix_url())
    return query_url

def build_svc_url(params):
    url = str(svc.get_svc_base_url()) + build_query_url(params)
    return url

def parse_gene_node_parameters(params):
    separator = ";"
    result = str(separator.join(params))
    return result

params_map = {
  'proteinModification' : 'MODIFY',
  'ppiInteraction' : 'PPI',
  'cpi' : 'CPI',
  'geneExpressionRegulation' : 'GENEEXPREGU',
  'srnaRegulation' : 'SRNAREGU',
  'transportedMolecule' : 'MOLTRANSPORT',
  'composition' : 'COMPOSITION',
  'coexpressedGenePair' : 'COEXP',
}

def build_param_map(args, token):
    params = {}

    params['hasParams'] = 'T'
    # extract gene nodes
    genes = args['genes']
    list_gene_nodes = gi.get_nodes_by_genes(svc.gene_svc_url(), token, genes)
    nodes = parse_gene_node_parameters(list_gene_nodes)
    log.info("Target Nodes: {0}".format(nodes))
    if (nodes):
        params['nodes'] = nodes

   #extract other parameters
    for key, value in args.iteritems():
        if not (key == 'genes'):
            if key in ('pathalg', 'steps'):
                params[key] = value
            elif key == 'coexpValueCutoff':
                params['COEXP_value'] = value
            elif key == 'cutoffNodeRelationships':
                params['cutoffHubRels'] = value
            elif key in params_map.keys():
                _key = params_map[key]
                pred_key = "{0}_predicted".format(_key)
                pred_value = 'T' if args['showPredictedEdge'] else 'F'
                val_key = "{0}_validated".format(_key)
                val_value = 'T' if args['showValidatedEdge'] else 'F'
                params[pred_key], params[val_key] = pred_value, val_value

                if _key == 'SRNAREGU' and not args['showsrnaRegulationPredicted']:
                    params[pred_key] = 'F'
                if _key == 'MODIFY' and not args['showppiInteractionPredicted']:
                    params[pred_key] = 'F'

            params['format'] = 'json'

    return params
