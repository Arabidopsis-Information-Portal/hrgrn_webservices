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
Main Module
"""

import json
import requests
import logging
import service as svc
import request_handler as rh
from requests.exceptions import ConnectionError
import exception

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# This function acts as a search endpoint
def search(args):
    """Retrieves search path between two gene nodes by gene/locus ID
     if all of target genes present, empty response otherwise.
     Note: search will be abandoned immediately once there is no gene node found 
     Acceptsno more than two gene IDs
     required parameters:  
    
     genes
                
     :rtype: response json
     :return: Returns a response object from the webservice in the json format if success raises exception otherwise
    
    """
    
    genes = args['genes']
   
    # get search service url
    token = args['_token']
    svc_url = svc.get_svc_base_url()

    try:
            # execute request
            response = rh.build_payload(svc_url, token, args)
            print json.dumps(response)
            print '---'
    except ValueError as e:
         error_msg = "Value Error:" + e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)
    except requests.exceptions.HTTPError as e:
         error_msg = "HTTP Error:" + e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)
    except ConnectionError as e:
         error_msg = "Connection Error:" + e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)
    except exception.NotFound as e:
         error_msg = e.message
         log.error(error_msg, exc_info=True)
         response = "{}"
         print json.loads(response)
         print '---'
    except exception.InvalidParameter as e:
         error_msg = e.message
         log.error(error_msg, exc_info=True)
         raise exception.InvalidParameter(error_msg)
    except exception.EmptyResponse as e:
         error_msg = e.message
         log.error(error_msg, exc_info=True)
         raise exception.EmptyResponse(error_msg)
    except Exception as e:
         error_msg = e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)

# This function acts as a list endpoint
def list(args):
     raise Exception('Not implemented yet')
