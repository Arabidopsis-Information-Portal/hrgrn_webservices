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
API Exception Module
"""


import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


no_geneID_parameter_error_msg = "No geneID/locus has been submitted!"
no_geneID_error_msg = "No node information found for geneID: "

# This function creates Not Found Exception 
class NotFound(Exception):
    pass

# This function creates Invalid Parameter Exception 
class InvalidParameter(Exception):
    pass

# This function creates Empty Response Exception 
class EmptyResponse(Exception):
    pass

# This function parses ADAMA API Exception 
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
            message = message[len('API error')+1:len(message)]
            log.debug("Error message:" + message)

    return message
