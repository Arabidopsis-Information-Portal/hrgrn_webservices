# file: request_builder.py

import requests
import json
import demjson
import logging
import timer as timer
from requests.exceptions import ConnectionError
import request_builder as rb
import exception

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

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

def build_payload(url, params, session, **kwargs):
    try:
        with timer.Timer() as t:
            headers = { 'Accept-Encoding': 'gzip,deflate', 'content-type': 'text/plain'}
            transformed_params = rb.build_param_map(params)
            response = session.get(url, params = transformed_params, headers=headers)
            response.raise_for_status()

            log.debug("Response Text:")
            log.debug(response.text)

            # get geneID/locus
            geneID = rb.getGeneID(params)

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
