# file: request_builder.py

import json
import logging
import request_builder as rb
import requests


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def handle_request(url, token, params, **kwargs):
    
    # add authorization headers if present
    headers = {}
    if token:
        headers["Authorization"] = "Bearer %s" % token
    response = requests.get(url, headers=headers, params=params)

    # Raise exception and abort if requests is not successful
    response.raise_for_status()
    
    try:
        # Try to convert result to JSON
        # abort if not possible
        return response.json()
    except ValueError:
        raise Exception('not a JSON object: {}'.format(response.text))

def build_payload(url, token, params, **kwargs):
    headers = { 'Accept-Encoding': 'gzip,deflate', 'content-type': 'text/plain'}
    
    transformed_params = rb.build_param_map(params, token)
    log.debug("Transformed params: {0}".format(transformed_params))
    
    response = requests.get(url, params=transformed_params, headers=headers)
    log.debug("Response Text:")
    log.debug(response.text)
    
    response.raise_for_status()
    
    # Raise exception and abort if requests is not successful
    parsed_response = json.loads(response.text)
    return parsed_response
