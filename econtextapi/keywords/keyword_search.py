import requests
import json
import logging

from econtextapi.client import Client
from econtextapi.keywords.search import Search

log = logging.getLogger('econtext')

class KeywordSearch(Search):
    
    qtype = 1
    
    def set_term(self, term):
        self.query['query'] = term
    
    def get_term(self):
        return self.query.get('query')
    
    def build_query(self, term=None, filters=None):
        """
        @param categories: A dictionary of {category_id: include_branch} pairs
        """
        if self.query.get('query') is not None and term is None:
            term = self.query.get('query')
        if self.query.get('filters') is not None and filters is None:
            filters = self.query.get('filters').get('filters')
        self.set_term(term)
        self.set_filters(filters)
        return self.query
    
    def search(self, term=None, filters=None):
        """
        @param term: The search term to look for
        """
        self.build_query(term, filters)
        log.debug("query: {}".format(json.dumps(self.query)))
        self.client.post(self)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--phrase", dest="phrase", required=True, action="store", default=None, help="Search phrase")
    parser.add_argument("-u", dest="username", required=True, action="store", default=None, help="API username")
    parser.add_argument("-p", dest="password", required=True, action="store", default=None, help="API password")
    parser.add_argument("-f", "--filter", dest="filter", default=None, help="Add a filter", metavar="JSON")
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
    
    filters = []
    if options.filter:
        filters.append(json.loads(options.filter))
    
    client = Client(options.username, options.password)
    search = KeywordSearch(client, pagesize=27, limit=100)
    search.set_term(options.phrase)
    page = search.retrieve_page()
    print("Total Results: {:>10}".format(search.count))
    print("        Pages: {:>10}".format(search.pages))
    print("    Page size: {:>10}".format(search.pagesize))
    
    result_pages = list(search.yield_pages())
    for page in result_pages:
        keywords = page.get_keywords()
        print("Page {}: {} keywords".format(page.page, len(keywords)))
        
    return True
    

if __name__ == "__main__":
    main()
