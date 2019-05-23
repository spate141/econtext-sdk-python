#! /usr/bin/python

usage = """
Quickly classify lots of social posts by distributing across multiple processors.

Input file should be a simple text file with one social post per line.

Be careful not to use too many workers at once - at some point it will end up
putting too much pressure on the API.  Use common sense.
"""

import argparse
import sys
import logging
import json
import time

import multiprocessing
from econtextapi.client import Client
from econtextapi.classify import Social

log = logging.getLogger('econtext')

def get_log_level(v=0):
    if v is None or v == 0:
        return logging.ERROR
    elif v > 1:
        return logging.DEBUG
    elif v > 0:
        return logging.INFO

def get_log(v):
    log_level = get_log_level(v)
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(process)s - %(asctime)s - %(levelname)s :: %(message)s", "%Y-%m-%d %H:%M:%S"))
    log.addHandler(h)
    h.setLevel(log_level)
    log.setLevel(log_level)

def f(x):
    """
    classify a set of social posts and block until you get the results - print 
    them when you get the output
    
    @param x: a list of up to 1000 posts
    """
    section, classify = x
    log.debug("classify/social with {} posts".format(len(classify.classify_data)))
    try:
        response = classify.classify()
    except:
        response = classify
    return section, response

def ff(x):
    return "ff(x): {}".format(x)

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]


def main():
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument("-i", "--in", dest="infile", default="stdin", help="Input file", metavar="PATH")
    parser.add_argument("-o", "--out", dest="outfile", default="stdout", help="Output file", metavar="PATH")
    parser.add_argument("-u", dest="username", required=True, action="store", default=None, help="API username")
    parser.add_argument("-p", dest="password", required=True, action="store", default=None, help="API password")
    parser.add_argument("-w", dest="workers", action="store", default=1, help="How many worker processes to use")
    parser.add_argument("-v", dest="config_verbose", action="count", default=0, help="Be more or less verbose")
    options = parser.parse_args()
    get_log(options.config_verbose)
    
    log.info("Running classification using {} worker processes".format(options.workers))
    
    if options.infile == 'stdin':
        infile = sys.stdin
    else:
        infile = open(options.infile, 'r')
    if options.outfile == 'stdout':
        outfile = sys.stdout
    else:
        outfile = open(options.outfile, 'w')
    
    posts = list(chunks([k.strip() for k in infile], 1000))
    log.info("Total post sections: {}".format(len(posts)))
    
    client = Client(options.username, options.password)
    poolInput = ((i, Social(client, posts[i])) for i in range(0, len(posts)))
    
    start = time.time()
    p = multiprocessing.Pool(processes=int(options.workers))
    resultset = p.imap_unordered(f, poolInput)
    
    s = 0
    k = 0
    with outfile as file:
        for (section, classification) in resultset:
            s = s + 1
            log.debug("Processing set {}".format(section+1))
            if classification.result is None:
                continue
            k = k + len(classification.result['results'])
            i = 0
            for mapping in classification.result['results']:
                mapping["post"] = posts[section][i]
                file.write("{}\n".format(json.dumps(mapping)))
                i = i + 1
    
    elapsed = time.time()-start
    log.info("Total time: {}".format(elapsed))
    log.info("Total keywords: {}".format(k))
    log.info("Total sets: {}".format(s))
    log.info("Time per 10k keywords: {}".format(elapsed/(k+.000000001) * 10000))
    return True
    

if __name__ == "__main__":
    main()
