"""
Utility functions for the API
"""

import collections

def get_category_path(category):
    if category is None:
        return None
    return "->".join(category['path'])

def second_to_last(l):
    """
    return the second to last item in a list with a little bit of logic in case
    thats not possible
    """
    if len(l) < 1:
        return None
    if len(l) < 2:
        return l[-1]
    else:
        return l[-2]

def group_by_ancestors(categories, depth=3):
    """
    Group a list of categories by a certain path depth (starting from the front)
    """
    d = collections.defaultdict(list)
    for c in categories:
        d['::'.join(c['path'][0:depth])].append(c)
    return d

