# HRGRN WebServices
# Copyright (C) 2016  Xinbin Dai, Irina Belyaeva

# This file is part of HRGRN WebServices API.
#
# HRGRN API is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# HRGRN API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with HRGRN API.  If not, see <http://www.gnu.org/licenses/>.

"""
Gene Info Service API. Provides search for a gene node ID by a gene/locus identifier
"""

import logging

import exception
import request_builder as rb
import request_handler as rh


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# This function retrieves a gene node ID  by a gene/locus ID
def get_node_by_gene_id(url, token, params):
    """ Retrieve  a gene node ID  by a gene/locus ID
    from passed service url and parameters
          
    :type url: string
    :param url: The gene info service url
      
    :type params: dict
    :param params: The dictionary(map) of parameters submitted via query string 
       
    :rtype: json like string
    :return: Returns gene node as json-like string
    
    """
    log.debug(url)

    # get geneID/locus
    geneID = rb.get_gene_id(params)
    log.debug("Gene ID:" + str(geneID))

    #get gene node info in json format from the gene_node_info service
    response = rh.handle_request(url, token, params)

    log.debug("Response:")
    log.debug(response)

    if not response:
        log.error("Empty Response!")
        log.debug(response.text)
        raise exception.EmptyResponse("No response received for geneID/locus: " + str(geneID))
    
    #get node id from the response return not found exception otherwise
    try:
             node_id = response["result"][0][0]['data']['id']

             if not node_id:
                 raise exception.NotFound(exception.no_geneID_error_msg + geneID)

    except Exception as e:
             raise exception.NotFound(exception.no_geneID_error_msg + geneID)
         
    
    return node_id

# get all gene nodes as list of json objects
def get_nodes_by_genes(url, token, params):
    """ Retrieve  all gene nodes
    from passed service url and parameters
         
    :type url: string
    :param url: The gene info service url
      
    :type params: dict
    :param params: The dictionary(map) of parameters submitted via query string 
       
    :rtype: list
    :return: Returns list of json objects
    
    """
    
    log.debug("Get Nodes by Genes has started.")
    
    target_genes = params.split(',')
    
    nodes = []
    
    # iterate over genes of interest
    for item in target_genes:
       gene_params = { 'locus' : item }
       log.debug("Gene:" + item)
       node = get_node_by_gene_id(url, token, gene_params)
       if (node):
           nodes.append(node)
    return nodes
