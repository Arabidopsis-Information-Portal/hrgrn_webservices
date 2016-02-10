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
Builds Request Parameters from a query string
"""

import json
import logging
import service as svc
import gene_info_service as gi
import exception

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

# This function transforms a list of gene identifiers to string of identifiers separated by a semicolon
def parse_gene_node_parameters(params):
    """Create a string of gene identifiers separated by a semicolon 
    
    :type params: list
    :param name: The list of gene identifiers
    
    :rtype: string
    :return: Returns gene identifiers separated by a semicolon
    
    """  
    separator = ";"
    result = str(separator.join(params))
    return result

# This function builds a parameter map to pass to the underlying webservice
def build_param_map(args, token):
    """Build a parameter map,
    add default parameters
    validate parameters/values
    match passed parameters by name with parameters of the underlying service
    
    :type args: dict
    :param args: The dictionary(map) of parameters submitted via query string 
    
    :rtype: string
    :return: Returns parameter map that matches to the underlying webservice
    
    """
    params = {}

     # add default parameters
    params['hasParams']='T'
    params['format'] = 'json'
    
    # extract gene nodes from query url
    # validate parameters first using fail-first approach
    validateParameters(args)
    
    # extract gene nodes
    genes = args['genes']
    _url, _namespace = args['_url'], args['_namespace']
    
    list_gene_nodes = gi.get_nodes_by_genes(svc.gene_svc_url(url=_url, namespace=_namespace), \
        token, genes)

    if (list_gene_nodes) and len(list_gene_nodes)==2:
        params['node1'] = list_gene_nodes[0]
        params['node2'] = list_gene_nodes[1]

        log.info("Node1:" +str(list_gene_nodes[0]))
        log.info("Node2:" +str(list_gene_nodes[1]))

    else:
        raise Exception("Only two genes can be submitted!")

   #extract other parameters
    for key, value in args.iteritems():
        # skip genes parameter, we already mapped it over
         if not (key == 'genes'):
             # map edge type parameters
             if ((key in edge_type_params_map.keys()) and value=='true'):
                 _boolean_key = edge_type_params_map[key]
                 params[_boolean_key] = 'T'
                 log.debug("Edge Type Key:" + _boolean_key + ";Edge Type Value:" + value)

             if key in param_value_map.keys():
                 _key = param_value_map[key]
                 params[_key] = value
                 log.debug("Parameter Key:" + _boolean_key + ";Parameter Value:" + value)

   
    return params

def get_gene_id(params):

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
    
    
# This function retrieves a gene identifier from a parameter map d
def validateParameters(params):
    """Retrieve a gene identifier if parameter locus is present,
    raise error otherwise
    
    :type params: dict
    :param params: genes locus identifiers  
    
    :raises: :class: 'exception.InvalidParameter
    
    :rtype: string
    :return: Returns a gene identifier
    
    """
    # key of locus parameter
    _key_geneID = 'genes'

    try:
        if not _key_geneID in params.keys():
            raise exception.InvalidParameter(exception.no_geneID_parameter_error_msg)
    except Exception as e:
        raise exception.InvalidParameter(exception.no_geneID_parameter_error_msg)
    
# This function validates if a parameter map has a requested key    
def has_param(params, param_key, error_msg):
    """Validate if a parameter map has a requested key
    raise error otherwise
    
    :type params: dict
    :param params: key/value a parameter map  
    
    :type param_key: string
    :param param_key: parameter key  
    
    :raises: :class: 'exception.InvalidParameter
    
    :rtype: True
    :return: Returns True if success
    
    """
    
    if not error_msg:
        error_msg = "No Parameter " + str(param_key) + " is present"
   
    log.debug("Param Key:" + param_key)
    
    if param_key in params.keys():
            return True
    else:
            raise exception.InvalidParameter(error_msg)

# This function validates if a key has a non-null value       
def has_value(_key, _value, error_msg):
    """Validate if a key has a non-null value
    raise error otherwise
    
    :type _key: string
    :param params: name of the parameter
    
    :type _value: string
    :param _value: value of the parameter 
    
    :raises: :class: 'exception.InvalidParameter
    
    :rtype: True
    :return: Returns True if success
    
    """
    
    if not error_msg:
        error_msg = "No Value for " + str(_key) + " is present"
       
    if _value:
        return True
    else:
            raise exception.InvalidParameter(error_msg)  
