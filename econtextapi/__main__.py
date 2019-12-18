#! /usr/bin/python

usage = """
The eContext API client:

Current iteration provides classification services for HTML and plaintext
classification and simply prints matched category names for the provided content.
"""

import argparse
import sys
import logging
import json

from econtextapi.client import Client
from econtextapi.classify.html import Html
from econtextapi.classify.text import Text
from econtextapi.classify.social import Social
from econtextapi.classify.url import Url
from econtextapi.classify.keywords import Keywords

log = logging.getLogger('econtextapi')

def get_log_level(v=0):
    if v is None or v == 0:
        return logging.ERROR
    elif v > 2:
        return logging.DEBUG
    elif v > 1:
        return logging.INFO
    elif v > 0:
        return logging.WARNING

def get_log(v):
    log_level = get_log_level(v)
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(process)s - %(asctime)s - %(levelname)s :: %(message)s", "%Y-%m-%d %H:%M:%S"))
    log.addHandler(h)
    h.setLevel(log_level)
    log.setLevel(log_level)


def main():
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument("-t", "--type", dest="type", action="store", default="html", help="What type of classification [html|text|social]")
    parser.add_argument("-i", "--in", dest="infile", action="store", default=None, help="Input file", metavar="PATH")
    parser.add_argument("-u", dest="username", required=True, action="store", default=None, help="API username")
    parser.add_argument("-p", dest="password", required=True, action="store", default=None, help="API password")
    parser.add_argument("-v", dest="config_verbose", action="count", default=0, help="Be more or less verbose")
    options = parser.parse_args()
    get_log(options.config_verbose)
    
    if options.infile is None:
        infile = sys.stdin
    else:
        infile = open(options.infile, 'r')
    
    client = Client(options.username, options.password)
    
    if options.type == "text":
        classify = Text(client, infile.read())
    #URL -- Classify a single URL
    elif options.type == "url":
        classify = Url(client, infile.read().strip())
    #KEYWORD -- Classify up to 1000 keywords (1 per line)
    elif options.type == "keywords":
        classify = Keywords(client, [kwd.strip() for kwd in infile.readlines()][:1000])
    #HTML -- Classify a single HTML document
    elif options.type == "html":
        classify = Html(client, infile.read())
    #SOCIAL -- Classify up to 1000 social posts (1 per line)
    elif options.type == "social":
        classify = Social(client, [social.strip() for social in infile.readlines()][:1000])
    else:
        raise NotImplementedError("{} classification not yet implemented".format(options.type))
    
    response = classify.classify()
    classify.print_summary()
        
    return True
    

if __name__ == "__main__":
    main()
