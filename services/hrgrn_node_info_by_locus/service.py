# file: service.py

import json
import requests
import re
import gzip
import StringIO
import zlib
import urllib2
import demjson
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def get_svc_base_url():
    return 'http://plantgrn.noble.org/hrgrn/nodes'
