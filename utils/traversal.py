# -*- coding: utf-8 -*-

import os

from gitoweb.settings import BASE_DIR


def item_traversal(dir):
    item_dict = {}
    l1_obj = []
    dir = dir.strip('/')
    dir_full = BASE_DIR + '/' + dir + '/'
    for l1_item in os.listdir(dir_full):
        l1_abs = dir_full + l1_item
        l1_obj.append(l1_item)
        item_dict[dir] = l1_obj
        if os.path.isdir(l1_abs):
            item_dict[l1_item] = os.listdir(l1_abs)
    return item_dict
