# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:13:29 2016
"""

from econtextapi.api_callable import ApiCallable
import json
import logging

log = logging.getLogger('econtextapi')


class Sentiment(ApiCallable):
    INNER_WRAPPER = 'nlp'
    PATH = '/nlp/sentiment'
    
    def __init__(self, client, input=None, *args, **kwargs):
        super(Sentiment, self).__init__()
        self.client = client
        self.input = input
        self.data = {'input': input}
        self.sentiment = []
        
    def get_path(self):
        return "".join([self.client.baseurl, Sentiment.PATH])
    
    def get_data(self):
        return self.data
    
    def get_results(self):
        self.client.post(self)
        return self.result.get('sentiment')
    
    def process_result(self, response_object):
        """
        Provide categories
        Provide posts: [ {'scored_categories':[...], 'scored_keywords':[...]}, ...]
        """
        super(Sentiment, self).process_result(response_object)
        self.sentiment = response_object['sentiment']
        return response_object
    
    def print_summary(self):
        self.client.post(self)
        print("sentiment")
        print(json.dumps(self.sentiment))

