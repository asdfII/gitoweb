# -*- coding: utf-8 -*-

import os
from math import ceil

from gitoweb.settings import BASE_DIR


def item_traversal(dir):
    item_dict = {}
    l1_list = []
    dir = dir.strip('/')
    dir_full = BASE_DIR + '/' + dir + '/'
    for l1_item in os.listdir(dir_full):
        l1_abs = dir_full + l1_item
        if l1_item[0] != '.':
            l1_list.append(l1_item)
            #~ l1_list.append(l1_abs)
            item_dict[dir] = l1_list
            if os.path.isdir(l1_abs):
                item_dict[l1_item] = os.listdir(l1_abs)
    return item_dict


def allowed_file(filename, extensions):
    ALLOWED_EXTENSIONS = set(extensions)
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class Pagination(object):
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count
    
    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))
    
    @property
    def has_prev(self):
        return self.page > 1
    
    @property
    def has_next(self):
        return self.page < self.pages
    
    def iter_pages(self,
        left_edge=2, left_current=2,
        right_current=5, right_edge=2
    ):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or (
                num > self.page - left_current - 1 and \
                num < self.page + right_current
            ) or num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
