# -*- coding: utf-8 -*-

import os

from gitoweb.settings import BASE_DIR


def item_traversal(dir):
    item_dict = {}
    l1_list = []
    dir = dir.strip('/')
    dir_full = BASE_DIR + '/' + dir + '/'
    for l1_item in os.listdir(dir_full):
        l1_abs = dir_full + l1_item
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
