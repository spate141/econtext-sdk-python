# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:13:29 2016
"""

from datetime import datetime
from econtextapi.client import Client
from econtextapi.api_callable import ApiCallable

import logging
log = logging.getLogger('econtext')

class Usage(ApiCallable):
    
    INNER_WRAPPER = 'user'
    PATH = '/user/usage'
    
    def __init__(self, client, start_date=None, end_date=None, *args, **kwargs):
        super(Usage, self).__init__()
        self.client = client
        self.result = None
        self.set_start_date(start_date)
        self.set_end_date(end_date)
    
    def get_path(self):
        return "".join([self.client.baseurl, Usage.PATH])
    
    def set_start_date(self, start_date=None):
        if not isinstance(start_date, (datetime, type(None))):
            raise TypeError("Expecting start_date to be a datetime object")
        self.start_date = start_date
        return self
    
    def set_end_date(self, end_date=None):
        if not isinstance(end_date, (datetime, type(None))):
            raise TypeError("Expecting start_date to be a datetime object")
        self.end_date = end_date
        return self
    
    def get_params(self):
        params = dict()
        if self.start_date is not None:
            params['start_date'] = self.start_date.strftime('%Y-%m-%d')
        if self.end_date is not None:
            params['end_date'] = self.end_date.strftime('%Y-%m-%d')
        return params
    
    def get_usage(self):
        self.client.get(self)
        return self.result.get('usage')
    
    def get_users(self):
        """
        Retrieve a list of users who have used the API in the given time period
        """
        self.client.get(self)
        return list(self.result.get('usage').keys())
    
    def get_total_usage(self):
        self.client.get(self)
        return self.result.get('total_usage')
    
    def get_users_totals(self):
        self.client.get(self)
        return dict((user, self.get_user_total(user)) for user in self.get_users())
    
    def get_user_usage(self, user):
        self.client.get(self)
        return self.result.get('usage').get(user)
    
    def get_user_total(self, user):
        self.client.get(self)
        user_usage = self.result.get('usage').get(user)
        if user_usage is None:
            return 0
        return sum(sum(x.values()) for x in list(user_usage.values()))
        
        
    def process_result(self, response_object):
        self.end_date = response_object['end_date']
        self.start_date = response_object['start_date']
        self.total_usage = response_object['total_usage']
        self.usage = response_object['usage']
        return response_object
        
    def print_summary(self):
        print("Total Usage Summary")
        print(" * period from {} to {}".format(self.result.get('start_date'), self.result.get('end_date')))
        print(" * overall usage: {}".format(self.get_total_usage()))
        print(" * usage by users:")
        for user, user_total in list(self.get_users_totals().items()):
            print("   - {:26}: {:>15}".format(user, user_total))

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", dest="username", required=True, action="store", default=None, help="API username")
    parser.add_argument("-p", dest="password", required=True, action="store", default=None, help="API password")
    parser.add_argument("-s", dest="start", required=False, action="store", default=None, help="Start Date (yyyy-mm-dd)")
    parser.add_argument("-e", dest="end", required=False, action="store", default=None, help="End Date (yyyy-mm-dd)")
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
    
    start_date = None
    if options.start is not None:
        start_date = datetime.strptime(options.start, '%Y-%m-%d')
        log.debug("Using start_date of {}".format(start_date.date()))
    
    end_date = None
    if options.end is not None:
        end_date = datetime.strptime(options.end, '%Y-%m-%d')
        log.debug("Using end_date of {}".format(end_date.date()))
    
    client = Client(options.username, options.password)
    usage = Usage(client).set_start_date(start_date).set_end_date(end_date)
    usage.get_usage()
    usage.print_summary()
        
    return True
    

if __name__ == "__main__":
    main()