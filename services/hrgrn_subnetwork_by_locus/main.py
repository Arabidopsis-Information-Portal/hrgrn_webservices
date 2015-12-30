# file: main.py
import json
import requests
import re
import gzip
import StringIO
import zlib
import urllib2
import demjson

def search(arg):
    genes = arg['genes']
    response_format = 'json'

    svc_url = build_svc_url(params)

    try:
            response = build_payload(svc_url)
            print json.dumps(response)
            print '---'
    except ValueError as e:
         print "ValueError:", e.message
    except requests.exceptions.HTTPError as e:
         print "HTTPError:", e.message

def list(args):
     raise Exception('Not implemented yet')

def transform_response(incoming_response):
    return demjson.decode(incoming_response.text)

def build_payload(url):
    headers = { 'Accept-Encoding': 'gzip,deflate', 'content-type': 'text/plain'}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return transform_response(r)

def get_svc_base_url():
    return 'http://plantgrn.noble.org/hrgrn/subnetwork?hasParams=T&'

def get_svc_suffix_url():
    svc_suffix = '&steps=2&pathalg=allSimplePaths&COMPOSITION_validated=T&COMPOSITION_predicted=T&MODIFY_validated=T&PPI_validated=T&CPI_validated=T&GENEEXPREGU_validated=T&SRNAREGU_validated=T&SRNAREGU_predicted=T&MOLTRANSPORT_validated=T&CHEMREACTION_validated=T&COEXP_predicted=T&COEXP_value=0.8&cutoffHubRels=100&format=json'
    return svc_suffix

def build_parameters(params):
    separator = ";"
    result = 'nodes=' + separator.join(params.split(','))
    return result

def build_query_url(params):
    query_url = str(build_parameters(params)) + str(get_svc_suffix_url())
    return query_url

def build_svc_url(params):
    url = str(get_svc_base_url()) + build_query_url(params)
    return url
