# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:13:29 2016
"""

from econtextapi.api_callable import ApiCallable
import json
import logging

log = logging.getLogger('econtext')


class Parse(ApiCallable):
    INNER_WRAPPER = 'nlp'
    PATH = '/nlp/parse'
    
    def __init__(self, client, doc_string=None, *args, **kwargs):
        super(Parse, self).__init__()
        self.client = client
        self.doc = doc_string
        
    def get_path(self):
        return "".join([self.client.baseurl, Parse.PATH])
    
    def get_data(self):
        return {
            'text': self.doc
        }
    
    def process_result(self, response_object):
        self.category = response_object['categories'][str(self.category_id)]
        return response_object
    
    def process_result(self, response_object):
        """
        Provide categories
        Provide posts: [ {'scored_categories':[...], 'scored_keywords':[...]}, ...]
        """
        super(Parse, self).process_result(response_object)
        self.doc = response_object['doc']
        return response_object
    
    def print_summary(self):
        self.client.post(self)
        print("Doc")
        print(json.dumps(self.doc))

