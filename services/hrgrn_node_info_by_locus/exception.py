# file: exception.py

class NotFound(Exception):
    pass

class InvalidParameter(Exception):
    pass

class EmptyResponse(Exception):
    pass


no_geneID_parameter_error_msg = "No geneID/locus has been submitted!"
no_geneID_error_msg = "No node information found for geneID: "
