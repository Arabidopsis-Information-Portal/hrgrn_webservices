# file: request_builder.py

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
            r = session.get(url, params = params, headers=headers)
            log.debug("Response Text:")
            log.debug(r.text)
            r.raise_for_status()
            #s = r.text.replace('\r', '\\r').replace('\n', '\\n')
            #log.info("s")
            #log.info(s)
            s = r.text
            parsed_response = json.loads(s.replace('\\', ''))


    finally:
        log.info('Response Building took %.03f sec.' % t.interval)
        log.info("Response Building has completed.")
    return parsed_response

def handle_request(url, params, **kwargs):

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
