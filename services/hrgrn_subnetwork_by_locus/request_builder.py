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

def get_param_list(params):
    return params.split(',')

def build_splitted_params(params, prefix):
   result = {}
   hasValidated = False
   hasPredicted = False
   list_params = params.split(',')
   for item in list_params:
       log.info("Item Param:" + item)
       if item == 'validated':
           hasValidated = True
       if item == 'predicted':
           hasPredicted = True

   if hasPredicted:
       result[prefix + '_predicted'] = 'T'
   else:
       result[prefix + '_predicted'] = 'F'

   if hasValidated:
       result[prefix + '_validated'] = 'T'
   else:
       result[prefix + '_validated'] = 'F'

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
                item_param_map= build_splitted_params(value, 'MODIFY')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'ppiInteraction':
                item_param_map= build_splitted_params(value, 'PPI')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'cpi':
                item_param_map= build_splitted_params(value, 'CPI')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'geneExpressionRegulation':
                item_param_map= build_splitted_params(value, 'GENEEXPREGU')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'srnaRegulation':
                item_param_map= build_splitted_params(value, 'SRNAREGU')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'transportedMolecule':
                item_param_map= build_splitted_params(value, 'MOLTRANSPORT')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'composition':
                item_param_map= build_splitted_params(value, 'COMPOSITION')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'coexpressedGenePair':
                item_param_map= build_splitted_params(value, 'COEXP')
                for item_key, item_value in item_param_map.iteritems():
                    params[item_key] = item_value
            elif key == 'coexpValueCutoff':
                params['COEXP_value'] = value
            elif key == 'cutoffNodeRelationships':
                params['cutoffHubRels'] = value

            params['format'] = 'json'

    return params