# file: request_builder.py

import json
import requests
import re
import gzip
import StringIO
import zlib
import urllib2
import demjson
import logging
import timer as timer
from requests.exceptions import ConnectionError
from requests_futures.sessions import FuturesSession
import request_builder as rb

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

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
            future_unparsed_result = session.get(url, params = transformed_params, headers=headers)
            r = future_unparsed_result.result()
            log.debug("Response Text:")
            log.debug(r.text)
            r.raise_for_status()
            parsed_response = transform_response(r)
    finally:
        log.info('Response Building took %.03f sec.' % t.interval)
        log.info("Response Building has completed.")
    return parsed_response
