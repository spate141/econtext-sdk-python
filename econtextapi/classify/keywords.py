# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 13:36:12 2016

"""

from econtextapi.classify.classify import Classify

class Keywords(Classify):
    
    PATH = "/keywords"
    
    def __init__(self, client, classify_data=None, *args, **kwargs):
        super(Keywords, self).__init__(client, 'keywords', classify_data)
    
    def get_path(self):
        return "".join([super(Keywords, self).get_path(), Keywords.PATH])
        
    def process_result(self, response_object):
        """
        Return maping
        Return associated_category
        """
        super(Keywords, self).process_result(response_object)
        self.mappings = response_object['mappings']
        return response_object
        
    def print_summary(self):
        print("Classifications: (time: {:.6} sec)".format(self.total_time()))
        i = 0
        for mappings in self.mappings:
            mappings = str(mappings)
            if mappings in self.categories:
                print(" * {:40} {:40}".format(self.classify_data[i][:40], self.categories[mappings]['name']))
            else:
                print(" * {:40} {:40}".format(self.classify_data[i][:40], ""))
            i += 1
        