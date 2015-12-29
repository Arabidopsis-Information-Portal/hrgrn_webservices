# file: main.py
import json
import requests
import re
import gzip
import StringIO
import zlib
import urllib2
import demjson

# Invoke HRGRN web services given a gene ID and output format parameters
# See http://plantgrn.noble.org/hrgrn/
# Example URI: http://plantgrn.noble.org/hrgrn/nodes?foreignID=AT3G46810&format=json

# Response: [
#    {data: {id:'np13163',label:'4CL.1',type:'Protein',tftr:'',tips:'4CL.1; 4CL1; AT4CL1, AT1G51680, ID=np13163, Protein',locus:'AT1G51680',shape:'ellipse',background_color:'#FCFCFC',border_color:'#585858',color:'#000000'} }
# ] which is invalid JSON

def search(arg):
    geneID = arg['geneID']
    response_format = 'json'

    svc_url = 'http://plantgrn.noble.org/hrgrn/nodes?foreignID=' + geneID + '&format=' + response_format

    try:
            response = build_payload(svc_url)
            response.raise_for_status()
            print json.dumps(response)
            print '---'
    except ValueError as e:
         print "ValueError:", e.message
    except requests.exceptions.HTTPError as e:
         print "HTTPError:", e.message

def list(args):
    raise Exception('Not implemented yet')

def transform_response(incoming_response):
    return demjson.decode(incoming_response)

def build_payload(url):
    r = requests.get(url)
    return transform_response(r)
