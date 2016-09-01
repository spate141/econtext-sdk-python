# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 11:00:12 2016

"""

from econtextapi.classify.html import Html

class Url(Html):
    
    PATH = "/url"
    
    def __init__(self, client, classify_data=None, *args, **kwargs):
        super(Html, self).__init__(client, 'url', classify_data)
    
    def get_path(self):
        return "".join([super(Html, self).get_path(), Url.PATH])
    