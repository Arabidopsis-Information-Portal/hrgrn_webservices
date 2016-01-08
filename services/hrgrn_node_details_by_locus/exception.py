# file: exception.py

import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class NotFound(Exception):
    pass

class InvalidParameter(Exception):
    pass

class EmptyResponse(Exception):
    pass

def parse_error(response):

    _key_message = 'message'

    if _key_message in response.keys():
        message = response[_key_message]

    index = -1

    if len(message) > 0:
        index = message.find(no_geneID_error_msg)
        log.debug("Index:" + str(index))
        message = message[index:len(message)]
        log.debug("Error message:" + message)

    return message

no_geneID_parameter_error_msg = "No geneID/locus has been submitted!"
no_geneID_error_msg = "No node information found for geneID: "
