# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:13:29 2016
"""

from datetime import datetime
from econtextapi.client import Client
from econtextapi.api_callable import ApiCallable

import logging
log = logging.getLogger('econtext')

class Category(ApiCallable):
    
    INNER_WRAPPER = u'category'
    PATH = u'/category/{}'
    
    def __init__(self, client, category_id=None, *args, **kwargs):
        super(Category, self).__init__()
        self.client = client
        self.category_id = category_id
    
    def get_path(self):
        return "".join([self.client.baseurl, Category.PATH.format(self.category_id)])
    
    def get_category(self):
        self.client.get(self)
        return self.result.get('category')
        
    def process_result(self, response_object):
        self.category = response_object['category']
        return response_object
        
    def print_summary(self):
        self.client.get(self)
        print "Category"
        print self.category

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", dest="username", required=True, action="store", default=None, help="API username")
    parser.add_argument("-p", dest="password", required=True, action="store", default=None, help="API password")
    parser.add_argument("-c", dest="category", required=True, action="store", default=None, help="ID of the category to retrieve")
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
    usage = Category(client, options.category)
    usage.get_category()
    usage.print_summary()
    return True
    

if __name__ == "__main__":
    main()