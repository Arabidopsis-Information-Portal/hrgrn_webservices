# file: exception.py

import logging


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class NotFound(Exception):
    pass

class InvalidParameter(Exception):
    pass

class EmptyResponse(Exception):
    pass

def parse_error(response):

    _key_message = 'message'

    _key_exception_type = 'exception'

    if _key_message in response.keys():
        message = response[_key_message]

    if _key_exception_type in response.keys():
        exception_type = response[_key_exception_type]

    index = -1

    if len(message) > 0 and exception_type == 'APIException':
        index = message.rfind('API error')
        log.debug("Index:" + str(index))
        if index > -1:
            message = message[len('API error') + 1:len(message)]
            log.debug("Error message:" + message)

    return message

no_geneID_parameter_error_msg = "No geneID/locus has been submitted!"
no_geneID_error_msg = "No node information found for geneID: "
