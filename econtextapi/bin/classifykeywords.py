#! /usr/bin/python
import threading

usage = """
Quickly classify lots of keywords by distributing across multiple processors.

Input file should be a simple text file with one keyword per line.

Be careful not to use too many workers at once - at some point it will end up
putting too much pressure on the API.  Use common sense.
"""

import argparse
import requests
import sys
import logging
import json
import csv
import time

from econtextapi.client import Client
from econtextapi.classify import Keywords
from econtext.util.files import ropen, sopen
from econtext.util.log import log


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


def f(classify):
    """
    classify a set of social posts and block until you get the results - print
    them when you get the output

    @param classify: a Classify object
    """
    try:
        response = classify.classify()
    except:
        log.exception()
        response = classify
    
    result = json.dumps({"input": classify.classify_data, "response": classify.response})
    return result


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
    parser.add_argument("-m", "--meta", dest="meta", default=None, help="Meta data to be included with each call", metavar="JSON")
    parser.add_argument("-b", "--base-url", dest="base_url", default="https://api.econtext.com/v2", help="Use a different base-url", metavar="URL")
    options = parser.parse_args()
    get_log(options.config_verbose)
    start = time.time()
    log.info("Running classification using {} worker processes".format(options.workers))
    
    infile = ropen(options.infile, batch_size=options.chunk_size)  # resumable input file
    if options.outfile == 'stdout':
        outfile = sys.stdout
    else:
        outfile = sopen(options.outfile, 'w')  # threadsafe output file
    
    stream_meta = None
    if options.meta:
        meta_file = open(options.meta)
        stream_meta = json.load(meta_file)
        log.debug("stream_meta: %s", json.dumps(stream_meta))
    
    client = Client(options.username, options.password, baseurl=options.base_url)
    
    def worker():
        while True:
            try:
                item = infile.readlines_batch()
                if not item:
                    break
                start_time = time.time()
                s = Keywords(client, item)
                s.data['stream_meta'] = stream_meta
                s.data['source_language'] = 'auto'
                response = f(s)
                outfile.write("{}\n".format(response))
                log.debug("classify/keywords with %s posts took %0.3f seconds", len(s.classify_data), (time.time() - start_time))
            except:
                break
    
    threads = []
    for i in range(int(options.workers)):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        pass
    finally:
        infile.close()
        outfile.close()
    
    elapsed = time.time() - start
    log.info("Total time: {}".format(elapsed))
    return True
    

if __name__ == "__main__":
    main()
