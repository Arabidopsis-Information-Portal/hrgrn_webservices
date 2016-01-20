# file: gene_info_service.py
import logging
import request_handler as rh
import request_builder as rb
import exception

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def get_node_by_gene_id(url, token, params):

    # get geneID/locus
    geneID = rb.getGeneID(params)

    response = rh.handle_request(url, token, params)

    log.debug("Response:")
    log.debug(response)

    if not response:
        log.error("Empty Response!")
        log.debug(response.text)
        raise exception.EmptyResponse("No response received for geneID/locus: " + str(geneID))

    if 'status' in response.keys():
        if response['status'] == 'error':
            error_msg = exception.parse_error(response)
            log.debug("Error message:" + error_msg)
            if exception.no_geneID_error_msg in error_msg:
                raise exception.NotFound(error_msg)
            else:
                raise Exception(error_msg)

    try:
             node_id = response["result"][0][0]['data']['id']

             if not node_id:
                 raise exception.NotFound(exception.no_geneID_error_msg + geneID)

    except Exception as e:
             raise exception.NotFound(exception.no_geneID_error_msg + geneID)


    return node_id

def get_nodes_by_genes(url, token, params):
    log.info("Get Nodes by Genes has started.")
    target_genes = params.split(',')
    nodes = []
    for item in target_genes:
       gene_params = {'locus':item}
       log.info("Gene:" + item)
       node = get_node_by_gene_id(url, token, gene_params)
       if (node):
           nodes.append(node)
    return nodes
