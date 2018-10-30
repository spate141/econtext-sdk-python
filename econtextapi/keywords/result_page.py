from econtextapi.api_callable import ApiCallable

class ResultPage(ApiCallable):
    
    INNER_WRAPPER = "keywords"
    
    def __init__(self, client, result_uri=None, page=1, *args, **kwargs):
        super(ResultPage, self).__init__(client)
        self.result_uri = result_uri
        self.page = page
        self.keywords = list()
        self.categories = dict()
    
    def process_result(self, response_object):
        super(ResultPage, self).process_result(response_object)
        self.keywords = response_object['keywords']
        self.categories = response_object['categories']
    
    def get_params(self):
        return {"page":self.page}
    
    def get_path(self):
        return self.result_uri
    
    def get_keywords(self):
        self.client.get(self)
        return self.keywords
    
    def get_categories(self):
        self.client.get(self)
        return self.categories