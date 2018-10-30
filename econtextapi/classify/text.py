from econtextapi.classify.classify import Classify

class Text(Classify):
    
    PATH = "/text"
    
    def __init__(self, client, classify_data=None, *args, **kwargs):
        super(Text, self).__init__(client, 'text', classify_data)
    
    def get_path(self):
        return "".join([super(Text, self).get_path(), Text.PATH])
    
    def process_result(self, response_object):
        """
        Provide scored_categories
        Provide scored_keywords
        """
        super(Text, self).process_result(response_object)
        self.scored_categories = response_object['scored_categories']
        self.scored_keywords = response_object['scored_keywords']
        return response_object
    
    def print_summary(self):
        print("Classifications:")
        for scored_category in self.scored_categories:
            print(" * {:40} {:5}".format(self.categories[str(scored_category['category_id'])]['name'], scored_category['score']))

