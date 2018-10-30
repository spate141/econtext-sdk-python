__author__="jspalink"
__date__ ="$Mar 25, 2015 1:27:41 PM$"

"""
Provides a common interface to the Classification calls in the API
"""

import requests
import json
import logging
import urllib.request, urllib.parse, urllib.error

from econtextapi import RESPONSE_WRAPPER
from econtextapi.client import Client
from econtextapi.api_callable import ApiCallable

log = logging.getLogger('econtext')

class Density(ApiCallable):
    """
    Density allows you to retrieve several categories given a single input 
    string
    
    1) GET a result object given an input string
    """
    
    INNER_WRAPPER = 'categories'
    PATH = '/categories/search'
    
    def __init__(self, client, term=None, limit=10, *args, **kwargs):
        """
        Create a Density Search object
        
        @param session A requests.session object with a valid authentication
        @param tries How many attempts to retrieve a result set
        @param delay How long to wait in between retrieval attempts
        """
        super(Density, self).__init__()
        self.client = client
        self.term = term
        self.limit = limit
    
    def set_term(self, term):
        self.term = term
        return self
    
    def set_limit(self, limit=10):
        if not isinstance(limit, int):
            raise ValueError("Expecting an integer limit")
        self.limit = limit
        return self
    
    def get_path(self):
        if self.term is None:
            raise ValueError("No search term specified")
        return "".join([self.client.baseurl, Density.PATH]) + "/{}".format(urllib.parse.quote(self.term))
    
    def get_params(self):
        params = {}
        if self.limit is not None:
            params['limit'] = self.limit
        return params
    
    def search(self, term=None, limit=10):
        """
        Provide classification for the input string
        """
        if self.term is not None and term is None:
            term = self.term
        self.set_term(term).set_limit(limit)
        return self.client.get(self)
    
    def process_result(self, response_object):
        """
        Allow us to provide customized return objects
        """
        self.categories = response_object
        return response_object
    
    def print_summary(self):
        self.client.get(self)
        print("Possible Classifications:")
        for category in self.categories:
            print(" * {:40} {:5}".format(category['name'], category['confidence']))
        
        for category in self.categories:
            print(" > ".join(category['path']))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--phrase", dest="phrase", required=True, action="store", default=None, help="Search phrase")
    parser.add_argument("-u", dest="username", required=True, action="store", default=None, help="API username")
    parser.add_argument("-p", dest="password", required=True, action="store", default=None, help="API password")
    parser.add_argument("-v", dest="verbose", action="store_true", default=False, help="Be verbose")
    options = parser.parse_args()
    
    def get_log(log_level=logging.DEBUG):
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter("%(process)s - %(asctime)s - %(levelname)s :: %(message)s", "%Y-%m-%d %H:%M:%S"))
        log.addHandler(h)
        h.setLevel(log_level)
        log.setLevel(log_level)
    
    if options.verbose:
        get_log(logging.DEBUG)
    
    client = Client(options.username, options.password)
    search = Density(client, options.phrase)
    search.print_summary()
        
    return True
    

if __name__ == "__main__":
    main()
