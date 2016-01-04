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
    return 'http://plantgrn.noble.org/hrgrn/element_detail'

def gene_svc_url():
    return 'https://api.araport.org/community/v0.3/hrgrn/hrgrn_node_info_by_locus_v0.3/search'
