'''
Wraps a requests.session object - this object can be passed along to a request
type and handles the connectivity to the API
'''

import requests
import logging
from json import dumps
from econtextapi import RESPONSE_WRAPPER
from time import time

log = logging.getLogger('econtext')

class Client(object):
    
    session = None
    
    def __init__(self, username, password, baseurl="https://api.econtext.com/v2", workers=1, *args, **kwargs):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.headers.update({
            'Content-type': 'application/json',
            'User-agent': 'eContext API Client (Python/1.0)'
        })
        self.set_baseurl(baseurl)
        self.workers = 0
        self.set_workers(workers)
    
    def set_baseurl(self, baseurl="https://api.econtext.com/v2"):
        self.baseurl = baseurl
        return self
    
    def set_workers(self, workers=1):
        self.set_workers = workers
        return self
    
    def __call_api(self, type, model):
        if model.is_called():
            return model.response
        try:
            log.debug("url:  {}".format(model.get_path()))
            model.stime = time()
            if type.upper() == 'GET':
                response = self.session.get(model.get_path(), params=model.get_params())
            elif type.upper() == 'POST':
                response = self.session.post(model.get_path(), data=dumps(model.get_data()))
            model.etime = time()
            model.response = response.json()
            model.set_called()
            response.raise_for_status()
        except Exception as e:
            log.error(e)
            if RESPONSE_WRAPPER not in model.response:
                log.error("ERROR: {}".format(model.response))
            else:
                error = model.response[RESPONSE_WRAPPER].get('error')
                if error is not None and 'code' in error and 'message' in error:
                    log.error("{}: {}".format(error['code'], error['message']))
            raise e
        model.result = model.process_result(model.response[RESPONSE_WRAPPER][model.INNER_WRAPPER])
        return model.response
    
    def get(self, model):
        # type: (object) -> object
        return self.__call_api('GET', model)
    
    def post(self, model):
        return self.__call_api('POST', model)
