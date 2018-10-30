
from econtextapi.classify.classify import Classify

class Social(Classify):
    
    PATH = "/social"
    
    def __init__(self, client, classify_data=None, *args, **kwargs):
        super(Social, self).__init__(client, 'social', classify_data)
    
    def get_path(self):
        return "".join([super(Social, self).get_path(), Social.PATH])
    
    def process_result(self, response_object):
        """
        Provide categories
        Provide posts: [ {'scored_categories':[...], 'scored_keywords':[...]}, ...]
        """
        super(Social, self).process_result(response_object)
        self.posts = [post for post in response_object['results']]
        return response_object
    
    def yield_summary(self):
        self.client.post(self)
        for i in range(0, len(self.classify_data)):
            post = self.posts[i]
            data = self.classify_data[i]
            yield " post: {}".format(data)
            for scored_category in post['scored_categories']:
                yield "   * {:5} - {:40}".format(scored_category['score'],
                                             self.categories[str(scored_category['category_id'])]['name'])

    def print_summary(self):
        self.client.post(self)
        print("Classifications:")
        for i in range(0, len(self.classify_data)):
            post = self.posts[i]
            data = self.classify_data[i]
            print((" POST: {}".format(data)))
            for scored_category in post['scored_categories']:
                print(("   * {:5} - {:40}".format(scored_category['score'], self.categories[str(scored_category['category_id'])]['name'])))
