# file: service.py

import os.path as op
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def get_svc_base_url():
    return 'http://plantgrn.noble.org/hrgrn/element_detail'

def gene_svc_url(url='https://api.araport.org/community/v0.3', namespace='hrgrn'):
    return op.join(url, namespace, 'hrgrn_node_info_by_locus_v0.7', 'search')
