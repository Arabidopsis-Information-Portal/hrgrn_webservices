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

    params['hasParams']='T'
    # extract gene nodes
    genes = args['genes']
    _url, _namespace = args['_url'], args['_namespace']
    list_gene_nodes = gi.get_nodes_by_genes(svc.gene_svc_url(url=_url, namespace=_namespace), \
        token, genes)
    #nodes = parse_gene_node_parameters(list_gene_nodes)

    if (list_gene_nodes) and len(list_gene_nodes)==2:
        params['node1'] = list_gene_nodes[0]
        params['node2'] = list_gene_nodes[1]

        log.info("Node1:" +str(list_gene_nodes[0]))
        log.info("Node2:" +str(list_gene_nodes[1]))

    else:
        raise Exception("Only two genes can be submitted!")

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
