# -*- coding: utf-8 -*-

import os


item_dict = {}
dir_L1 = []
dir_L2 = []
dir_L3 = []

items = os.walk('./conf')
for root, dirs, files in items:
    #~ print root
    #~ print dirs
    for _ in files:
        print os.path.dirname(os.path.abspath(_))
        print os.path.abspath(_)
