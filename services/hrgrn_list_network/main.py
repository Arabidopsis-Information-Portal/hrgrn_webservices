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
Main Module
"""

import json
import requests
import logging
import timer as timer
from requests.exceptions import ConnectionError
from requests import Session
import service as svc
import request_handler as rh

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# This function acts as a list endpoint
def list(args):
    session = Session()
    
    # get service url
    svc_url = svc.get_svc_base_url()

    params = {'listall': 'T', 'format':'json'}

    try:
        with timer.Timer() as t:
            log.info("Service URL:" + svc_url)
            # execute request
            response = rh.build_payload(svc_url, params, session)
            log.debug(response)

            if (response):
                for item in response:
                    print json.dumps(item, indent=3)
                    print '---'
            else:
                raise Exception("Response cannot be null!")
            
    except ValueError as e:
         error_msg = "ValueError Exception:" + e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)
    except requests.exceptions.HTTPError as e:
         error_msg = "HTTPError Exception:" + e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)
    except ConnectionError as e:
         error_msg = "ConnectionError Exception:" + e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)
    except Exception as e:
         error_msg = "GenericError Exception:" + e.message
         log.error(error_msg, exc_info=True)
         raise Exception(error_msg)
    finally:
            log.info('Request took %.03f sec.' % t.interval)
