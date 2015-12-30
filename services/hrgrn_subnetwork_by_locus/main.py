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
    geneID = arg['genes']
    response_format = 'json'

    svc_url = 'http://plantgrn.noble.org/hrgrn/nodes?foreignID=' + 'AT2G38470' + '&format=' + response_format

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
