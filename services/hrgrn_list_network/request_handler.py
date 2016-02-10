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
import re
import demjson
import logging
import timer as timer
from requests.exceptions import ConnectionError
import request_builder as rb

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# transforms response to json format
def transform_response(incoming_response, strictMode=False):
    try:
        with timer.Timer() as t:
            text = incoming_response.text
            log.debug("Response Text To Decode:")
            log.debug(text)
            log.info("Response Decoding has started.")
            decoded_text = demjson.decode(text, strict = strictMode)
    finally:
        log.info('Response JSON Decoding took %.03f sec.' % t.interval)
        log.info("Response Decoding has completed.")
    return decoded_text

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
            headers = { 'Accept-Encoding': 'gzip,deflate', 'content-type': 'text/plain'}
            
            # execute a request by passing completely mapped and validated request parameters
            response = session.get(url, params = params, headers=headers)
            log.debug("Response Text:")
            log.debug(response.text)
            
             # Raise exception and abort if requests is not successful
            response.raise_for_status()
            s = response.text
            
            # convert received response (json like string) in a valid json object
            parsed_response = json.loads(s.replace('\\', ''))

    finally:
        log.info('Response Building took %.03f sec.' % t.interval)
        log.info("Response Building has completed.")
    return parsed_response

# This function executes a request passing parameters to the underlying webservice
def handle_request(url, params, **kwargs):
    """Executes a request,
    pass parameters and optional parameters
    
    :type url: string
    :param url: request url
    
    :type token: string
    :param token: ARAPORT API token (internal parameter)
    
    :type params: string
    :param params: request parameters
    
    :type kwargs: string
    :param kwargs: optional request parameters
    
    :rtype: response json
    :return: Returns a response object from the webservice in the json format if success raises exception otherwise
    
    """

    headers = { 'Accept-Encoding': 'gzip,deflate', 'content-type': 'text/plain'}
    response = requests.get(url, headers=headers, params=params)

    # Raise exception and abort if requests is not successful
    response.raise_for_status()

    try:
        # Try to convert result to JSON
        # abort if not possible
        return response.json()
    except ValueError:
        raise Exception('not a JSON object: {}'.format(response.text))
