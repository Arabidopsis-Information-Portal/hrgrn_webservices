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

no_geneID_parameter_error_msg = "No geneID/locus has been submitted!"
no_geneID_error_msg = "No node information found for geneID: "

# This function creates Not Found Exception 
class NotFound(Exception):
    pass

# This function creates Invalid Parameter Exception 
class InvalidParameter(Exception):
    pass

# This function parses ADAMA API Exception 
class EmptyResponse(Exception):
    pass

