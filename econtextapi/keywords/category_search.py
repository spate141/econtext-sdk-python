import requests
import json
import logging

from econtextapi.client import Client
from econtextapi.keywords.search import Search

log = logging.getLogger('econtext')


class CategorySearch(Search):
    
    qtype = 0
    
    def set_categories(self, categories):
        if categories is None:
            return
        for (category_id, include_branch) in list(categories.items()):
            self.__add_category(category_id, include_branch)
    
    def get_term(self):
        return self.query.get('query')
    
    def build_query(self, categories=None, filters=None):
        """
        @param categories: A dictionary of {category_id: include_branch} pairs
        """
        if self.query.get('query') is not None and categories is None:
            categories = self.query.get('query')
        if self.query.get('filters') is not None and filters is None:
            filters = self.query.get('filters').get('filters')
        self.set_categories(categories)
        self.set_filters(filters)
        return self.query
    
    def search(self, categories=None, filters=None):
        """
        @param categories A dictionary of category_id:include_branch key-value pairs
        """
        self.build_query(categories, filters)
        log.debug("query: {}".format(json.dumps(self.query)))
        self.client.post(self)
    
    def __add_category(self, category_id, include_branch=True):
        self.query['query'][category_id] = bool(include_branch)
        return self

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", dest="category", required=True, action="store", default=None, help="Search category id")
    parser.add_argument("--branch", dest="branch", required=False, action="store", default=True, help="Include the whole branch in the search")
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
    search = CategorySearch(client, limit=100)
    search.set_categories({options.category: bool(options.branch)})
    page = search.retrieve_page()
    print("Total Results: {:>10}".format(search.count))
    print("        Pages: {:>10}".format(search.pages))
    print("    Page size: {:>10}".format(search.pagesize))
        
    return True
    

if __name__ == "__main__":
    main()
