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
Returns base urls for the underlying endpoints
"""

import os.path as op
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# This function returns the search by path base url
def get_svc_base_url():
    return 'http://plantgrn.noble.org/hrgrn/path'

# This function returns the hrgrn_node_info_by_locus base url
def gene_svc_url(url='https://api.araport.org/community/v0.3', namespace='hrgrn'):
    return op.join(url, namespace, 'hrgrn_node_info_by_locus_v0.9', 'search')
