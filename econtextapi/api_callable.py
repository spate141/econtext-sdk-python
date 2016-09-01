
class ApiCallable(object):
    
    def __init__(self, client=None):
        self.client = client
        self.called = False
        self.stime = None
        self.etime = None
        self.response = None
        self.result = None
    
    def set_called(self):
        self.called = True
    
    def is_called(self):
        return self.called == True
    
    def get_params(self):
        return None
    
    def get_data(self):
        return None
    
    def get_duration(self):
        if not self.is_called():
            return None
        return self.etime - self.stime
    
    def process_result(self, response_object):
        return response_object