# file: gene_info_service.py
import logging
import request_handler as rh

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def get_node_by_gene_id(url, token, params):
    log.info(url)
    response = rh.handle_request(url, token, params)
    node_id = response["result"][0][0]['data']['id']
    return node_id

def get_nodes_by_genes(url, token, params):
    log.info("Get Nodes by Genes has started.")
    target_genes = params.split(',')
    nodes = []
    for item in target_genes:
       gene_params = { 'locus' : item }
       log.info("Gene:" + item)
       node = get_node_by_gene_id(url, token, gene_params)
       if (node):
           nodes.append(node)
    return nodes
