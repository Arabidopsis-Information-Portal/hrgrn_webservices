
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
Executes Request and Builds Response Payload returned to a web-client
"""

import requests
import json
import logging
import timer as timer
from requests.exceptions import ConnectionError
import request_builder as rb
import exception

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# This builds a payload returned to a web-client in response of received request
def build_payload(url, params, session, **kwargs):
    """Build response payload for a request,
    pass parameters and optional parameters
    send external parameters for mapping and valiadtion
    parse json like string
    return json object
    
    :type url: string
    :param url: request url
    
    :type token: string
    :param token: ARAPORT API token (internal parameter)
    
    :type params: string
    :param params: request parameters
    
    :type kwargs: string
    :param kwargs: optional request parameters
    
    :rtype: response json
    :return: Returns actual response payload from the webservice in the json format if success raises exception otherwise
    
    """
    
    try:
        with timer.Timer() as t:
            # build  request parameters, set defaults, map external parameters
            headers = { 'Accept-Encoding': 'gzip,deflate', 'content-type': 'text/plain'}
            transformed_params = rb.build_param_map(params)
            
            # execute a request by passing completely mapped and validated request parameters
            response = session.get(url, params = transformed_params, headers=headers)
            log.debug("Response Text:")
            log.debug(response.text)
            
             # Raise exception and abort if requests is not successful
            response.raise_for_status()

            # get geneID/locus
            geneID = rb.get_gene_id(params)

            if not response:
                log.error("Empty Response!")
                log.debug(response.text)
                raise exception.EmptyResponse("No response received for geneID/locus: " + str(geneID))

            parsed_response = json.loads(response.text)

            log.debug("Parsed Response:")
            log.debug(parsed_response)

            log.debug("Response Length:" +str(len(parsed_response)))

            if len(parsed_response)==0:

                log.debug("Empty Parsed Response:")
                log.debug(parsed_response)
                raise exception.NotFound(exception.no_geneID_error_msg + geneID)

            # ensure geneID/locus node info available in the json, raise Not Found error otherwise

            try:
                 node_id = parsed_response[0]["data"]["id"]

                 if not node_id:
                     raise exception.NotFound(exception.no_geneID_error_msg + geneID)

            except Exception as e:
                 raise exception.NotFound(exception.no_geneID_error_msg + geneID)
    finally:
        log.info('Response Building took %.03f sec.' % t.interval)
        log.info("Response Building has completed.")
    return parsed_response
