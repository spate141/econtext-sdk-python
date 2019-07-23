usage = """
Quickly classify lots of urls by distributing across multiple threads.

Input file should be a simple text file with one URL per line.

Be careful not to use too many workers at once - at some point it will end up
putting too much pressure on the API.  Use common sense.
"""

import argparse
import sys
import logging
import json
import time

import threading
import queue

from econtextapi.client import Client
from econtextapi.classify import Url
from econtext.util.resumable_file import ropen

log = logging.getLogger('econtext.classify-url')


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
    s = time.time()
    try:
        response = classify.classify()
    except:
        response = classify
    
    result = json.dumps({"input": classify.classify_data, "response": classify.response})
    log.debug("classify/url took %0.3f seconds", (time.time() - s))
    return result


def ff(x):
    return "ff(x): {}".format(x)


def main():
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument("-i", "--in", dest="infile", default="stdin", help="Input file", metavar="PATH")
    parser.add_argument("-o", "--out", dest="outfile", default="stdout", help="Output file", metavar="PATH")
    parser.add_argument("-u", dest="username", required=True, action="store", default=None, help="API username")
    parser.add_argument("-p", dest="password", required=True, action="store", default=None, help="API password")
    parser.add_argument("-w", dest="workers", action="store", default=1, help="How many worker processes to use")
    parser.add_argument("-m", "--meta", dest="meta", default=None, help="Meta data to be included with each call", metavar="JSON")
    parser.add_argument("-v", dest="config_verbose", action="count", default=0, help="Be more or less verbose")
    options = parser.parse_args()
    get_log(options.config_verbose)
    
    start = time.time()
    log.info("Running classification using {} worker processes".format(options.workers))
    
    if options.infile == 'stdin':
        infile = sys.stdin
    else:
        infile = ropen(options.infile)
    if options.outfile == 'stdout':
        outfile = sys.stdout
    else:
        outfile = open(options.outfile, 'w')
    
    stream_meta = None
    if options.meta:
        meta_file = open(options.meta)
        stream_meta = json.load(meta_file)
        log.debug("stream_meta: %s", json.dumps(stream_meta))
    
    q = queue.Queue(int(options.workers))
    r = queue.Queue()  # result queue
    client = Client(options.username, options.password)
    
    def worker():
        while True:
            item = q.get()
            if item is None:
                break
            response = f(item)
            r.put(response)
            q.task_done()
    
    def output_worker():
        while True:
            item = r.get()
            if item is None:
                break
            outfile.write(item)
            outfile.write("\n")
            r.task_done()
    
    threads = []
    for i in range(int(options.workers)):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    printer = threading.Thread(target=output_worker)
    printer.start()
    
    while True:
        try:
            x = next(infile).rstrip()
        except:
            break
        
        u = Url(client, x)
        u.data['stream_meta'] = stream_meta
        u.data['source_language'] = 'auto'
        q.put(u)
    
    q.join()
    for i in range(int(options.workers)):
        q.put(None)
    
    r.join()
    r.put(None)
    for t in threads:
        t.join()
    printer.join()
    
    elapsed = time.time() - start
    log.info("Total time: {}".format(elapsed))
    return True


if __name__ == "__main__":
    main()
