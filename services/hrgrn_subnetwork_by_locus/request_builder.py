# file: request_builder.py
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
import gene_info_service as gi

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def parse_gene_node_parameters(params):
    separator = ";"
    result = str(separator.join(params))
    return result

def get_param_list(params):
    return params.split(',')

def build_splitted_params(args, params, prefix):
   result = {}

   hasValidated = args['showValidatedEdge']
   hasPredicted = args['showPredictedEdge']

   hasProteinToProteinInteractionPredicted = args['showppiInteractionPredicted']
   hasSrnaRegulationPredictedPredicted = args['showsrnaRegulationPredicted']

   if not (hasValidated):
       hasValidated = True

   if not (hasPredicted):
       hasPredicted = True

   if hasPredicted:
       result[prefix + '_predicted'] = 'T'
   else:
       result[prefix + '_predicted'] = 'F'

   if hasValidated:
       result[prefix + '_validated'] = 'T'
   else:
       result[prefix + '_validated'] = 'F'

   # override individual data filters
   if prefix == 'SRNAREGU' and not hasSrnaRegulationPredictedPredicted:
       result[prefix + '_predicted'] = 'F'

   if prefix == 'MODIFY' and not hasProteinToProteinInteractionPredicted:
       result[prefix + '_predicted'] = 'F'

   return result

def build_param_map(args, token):
    params = {}

    params['hasParams']='T'
    # extract gene nodes
    genes = args['genes']
    list_gene_nodes = gi.get_nodes_by_genes(svc.gene_svc_url(), token, genes)
    nodes = parse_gene_node_parameters(list_gene_nodes)
    log.info("Target Nodes:" + nodes)
    if (nodes):
        params['nodes'] = nodes

   #extract other parameters
    for key, value in args.iteritems():
        if not (key == 'genes'):
            if key in ('pathalg', 'steps'):
                params[key] = value

            elif key == 'proteinModification':
                item_param_map= build_splitted_params(args, value, 'MODIFY')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'ppiInteraction':
                item_param_map= build_splitted_params(args, value, 'PPI')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'cpi':
                item_param_map= build_splitted_params(args, value, 'CPI')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'geneExpressionRegulation':
                item_param_map= build_splitted_params(args, value, 'GENEEXPREGU')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'srnaRegulation':
                item_param_map= build_splitted_params(args, value, 'SRNAREGU')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'transportedMolecule':
                item_param_map= build_splitted_params(args, value, 'MOLTRANSPORT')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'composition':
                item_param_map= build_splitted_params(args, value, 'COMPOSITION')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'coexpressedGenePair':
                item_param_map= build_splitted_params(args, value, 'COEXP')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'coexpValueCutoff':
                params['COEXP_value'] = value
            elif key == 'cutoffNodeRelationships':
                params['cutoffHubRels'] = value

            params['format'] = 'json'

    return params
