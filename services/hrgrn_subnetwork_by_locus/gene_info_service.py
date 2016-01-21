# file: gene_info_service.py
import logging
import logging

import exception
import request_builder as rb
import request_handler as rh


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def get_node_by_gene_id(url, token, params):
    log.debug(url)

    # get geneID/locus
    geneID = rb.getGeneID(params)
    log.debug("Gene ID:" + str(geneID))

    response = rh.handle_request(url, token, params)

    log.debug("Response:")
    log.debug(response)

    if not response:
        log.error("Empty Response!")
        log.debug(response.text)
        raise exception.EmptyResponse("No response received for geneID/locus: " + str(geneID))
    
    try:
             node_id = response["result"][0][0]['data']['id']

             if not node_id:
                 raise exception.NotFound(exception.no_geneID_error_msg + geneID)

    except Exception as e:
             raise exception.NotFound(exception.no_geneID_error_msg + geneID)
         
    
    return node_id

def get_nodes_by_genes(url, token, params):
    log.debug("Get Nodes by Genes has started.")
    
    target_genes = params.split(',')
    
    nodes = []
    
    for item in target_genes:
       gene_params = { 'locus' : item }
       log.debug("Gene:" + item)
       node = get_node_by_gene_id(url, token, gene_params)
       if (node):
           nodes.append(node)
    return nodes
