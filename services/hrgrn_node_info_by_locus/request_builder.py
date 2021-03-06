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

import logging
import exception

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# This function builds a parameter map to pass to the underlying webservice
def build_param_map(args):
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
    params['format'] = 'json'
    
    # extract gene nodes from query url
    # validate parameters first using fail-first approach
    validateParameters(args)

    # extract gene/locus ID
    for key, value in args.iteritems():
        if (key == 'locus'):
            params['foreignID'] = value
        else:
            params[key] = value

    
    return params

# This function retrieves a gene identifier from a parameter map
def validateParameters(params):
    """Retrieve a gene identifier if parameter locus is present,
    raise error otherwise
    
    :type params: dict
    :param params: key/value of a locus identifier  
    
    :raises: :class: 'exception.InvalidParameter
    
    :rtype: string
    :return: Returns a gene identifier
    
    """
    # key of locus parameter
    _key_geneID = 'locus'

    try:
        if not _key_geneID in params.keys():
            raise exception.InvalidParameter(exception.no_geneID_parameter_error_msg)
    except Exception as e:
        raise exception.InvalidParameter(exception.no_geneID_parameter_error_msg)

# This function builds a parameter map to pass to the underlying webservice
def get_gene_id(params):
    """Retrieve a gene identifier if parameter locus is present,
    raise error otherwise
    
    :type params: dict
    :param params: key/value of a locus identifier  
    
    :raises: :class: 'exception.InvalidParameter
    
    :rtype: string
    :return: Returns a gene identifier
    
    """

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
