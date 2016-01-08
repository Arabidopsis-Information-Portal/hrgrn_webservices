# file: request_builder.py

import requests
import demjson
import json
import logging
import request_builder as rb

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def handle_request(url, token, params, **kwargs):

    headers = {}
    if token:
        headers["Authorization"] = "Bearer %s" % token
    response = requests.get(url, headers=headers, params=params)

    # Raise exception and abort if requests is not successful
    #response.raise_for_status()
    # we parse error in the get_node_by_id instead

    try:
        # Try to convert result to JSON
        # abort if not possible
        return response.json()
    except ValueError:
        raise Exception('not a JSON object: {}'.format(response.text))

def transform_response(incoming_response):
    log.info(incoming_response.text)
    return demjson.decode(incoming_response.text)

def build_payload(url, token, params, **kwargs):
    headers = { 'Accept-Encoding': 'gzip,deflate', 'content-type': 'text/plain'}
    transformed_params = rb.build_param_map(params, token)
    log.info("Transformed_params: {0}".format(transformed_params))
    r = requests.get(url, params=transformed_params, headers=headers)
    log.debug("Response Text:")
    log.debug(r.text)
    r.raise_for_status()
    parsed_response = json.loads(r.text)
    return parsed_response
