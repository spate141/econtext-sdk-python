__author__="jspalink"
__date__ ="$Mar 25, 2015 1:27:41 PM$"

"""
Provides a common interface to the Classification calls in the API
"""

import logging
from econtextapi.api_callable import ApiCallable

class Classify(ApiCallable):
    """
    Classify is an abstract object that contains data to be classified.  There
    are several different types of data that may be classified which are each
    implemented separately.  However, the procedure is the same.
    
    1) POST to the API the data to be classified
    2) GET the result object that the API provides
       a) if the result object is not complete, repeat 2
       b) if the result object is complete, return the result object
    """
    
    INNER_WRAPPER = u'classify'
    PATH = "/classify"
    
    def __init__(self, client, classify_field, classify_data=None, *args, **kwargs):
        """
        Create a classification object
        
        @param client an econtextapi.client object containing valid authentication
        """
        super(Classify, self).__init__()
        self.client = client
        self.data = {"async":False}
        self.classify_field = classify_field
        self.classify_data = classify_data
        self.time = {"start":None, "end":None}
        
    def get_path(self):
        return "".join([self.client.baseurl, Classify.PATH])
    
    def set_classify_field(self, field):
        self.classify_field = field
    
    def set_classify_data(self, data):
        self.classify_data = data
    
    def get_data(self):
        data = self.data
        data[self.classify_field] = self.classify_data
        return data
    
    def classify(self):
        """
        Classify a set of data
        """
        self.client.post(self)
        return self
    
    def get_categories(self):
        self.client.post(self)
        return self.result.get('categories')
    
    def get_results(self):
        self.client.post(self)
        return self.result.get('results')
    
    def total_time(self):
        return self.get_duration()
    
    def process_result(self, response_object):
        """
        Allow us to provide customized return objects
        """
        super(Classify, self).process_result(response_object)
        self.categories = response_object['categories']
        return response_object
