import requests
import json
import logging
log = logging.getLogger('econtext')


from econtextapi import RESPONSE_WRAPPER
from econtextapi.api_callable import ApiCallable
from econtextapi.keywords.result_page import ResultPage
from econtextapi.util import *

class Search(ApiCallable):
    """
    Create an object to search for keywords.  There are two types of keyword
    searches.
    
    1) Phrase Searches - Perform a keyword phrase search
    2) Category Searches - search for a list of categories (or their branches)
    
    This class exists as a super class that should be implemented for each of
    the above.
    """
    
    INNER_WRAPPER = u'keywords'
    PATH = u'/keywords/search'
    SEARCH_PAGE_LIMIT = 10000
    SEARCH_LIMIT = 500000
    
    def __init__(self, client, pagesize=10000, limit=500000, *args, **kwargs):
        """
        Create a Keyword Search object
        
        @param session A requests.session object with a valid authentication
        @param tries How many attempts to retrieve a result set
        @param delay How long to wait in between retrieval attempts
        """
        super(Search, self).__init__(client)
        self.pagesize = min(pagesize, Search.SEARCH_PAGE_LIMIT)
        self.limit = min(limit, Search.SEARCH_LIMIT)
        self.query = self.initialize_query(qtype=self.qtype, pagesize=self.pagesize, limit=self.limit)
    
    def initialize_query(self, query=None, qtype=0, filters=None, pagesize=10000, limit=500000, *args, **kwargs):
        if query is None:
            query = dict()
        if filters is None:
            filters = dict()
        search = {
            "query":query,
            "type":qtype,
            "pagesize":pagesize,
            "limit":limit,
            "filters":filters
        }
        return search
    
    def get_path(self):
        return "".join([self.client.baseurl, Search.PATH])
    
    def set_filters(self, filters):
        if filters is None:
            return
        for filter in filters:
            self.__add_filter(filter)
    
    def build_query(self, *args, **kwargs):
        raise NotImplementedError()
    
    def get_data(self):
        if self.query is None:
            raise ValueError("No query could be found")
        return self.query
    
    def __add_filter(self, filter):
        """
        For now - we're directly passing in an object
        """
        if 'filters' not in self.query:
            self.query['filters'] = {'filters':[]}
        self.query['filters']['filters'].append(filter)
        return self
    
    def process_result(self, response_object):
        super(Search, self).process_result(response_object)
        self.pages = response_object['pages']
        self.result_uri = response_object['result_uri']
        self.search_id = response_object['searchid']
        self.pagesize = response_object['pagesize']
        self.count = response_object['count']
        return response_object
    
    def retrieve_page(self, page=1):
        """
        Retrieve a single page from the result set
        """
        self.client.post(self)
        page = ResultPage(self.client, self.result_uri, page)
        return page
    
    def yield_pages(self, *args, **kwargs):
        """
        Retrieve results from the keywords search call
        """
        self.client.post(self)
        for page in xrange(1, self.pages+1):
            result_page = self.retrieve_page(page)
            yield result_page

