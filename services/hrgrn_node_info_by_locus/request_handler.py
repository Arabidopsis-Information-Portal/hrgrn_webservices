# file: request_builder.py

import requests
import json
import demjson
import logging
import timer as timer
from requests.exceptions import ConnectionError
import request_builder as rb

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
            r = session.get(url, params = transformed_params, headers=headers)
            log.debug("Response Text:")
            log.debug(r.text)
            r.raise_for_status()
            parsed_response = json.loads(r.text)
    finally:
        log.info('Response Building took %.03f sec.' % t.interval)
        log.info("Response Building has completed.")
    return parsed_response
