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
    params['format'] = 'json'
    
    return params
