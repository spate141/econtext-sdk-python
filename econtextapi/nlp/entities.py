# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:13:29 2016
"""

from econtextapi.api_callable import ApiCallable
import json
import logging

log = logging.getLogger('econtextapi')


class Entities(ApiCallable):
    INNER_WRAPPER = 'nlp'
    PATH = '/nlp/entities'
    
    def __init__(self, client, input=None, *args, **kwargs):
        super(Entities, self).__init__()
        self.client = client
        self.input = input
        self.data = {'input': input}
        self.entities = []
        
    def get_path(self):
        return "".join([self.client.baseurl, Entities.PATH])
    
    def get_data(self):
        return self.data
    
    def get_results(self):
        self.client.post(self)
        return self.result.get('entities')
    
    def process_result(self, response_object):
        """
        Provide categories
        Provide posts: [ {'scored_categories':[...], 'scored_keywords':[...]}, ...]
        """
        super(Entities, self).process_result(response_object)
        self.entities = response_object['entities']
        return response_object
    
    def print_summary(self):
        self.client.post(self)
        print("entities")
        print(json.dumps(self.entities))

