# -*- coding: utf-8 -*-

import os


#~ from gitoweb.settings import BASE_DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

item_dict = {}
l1_obj = []
l2_obj = []
l3_obj = []

for l1_item in os.listdir(BASE_DIR + '/conf/'):
    l1_abs = BASE_DIR + '/conf/' + l1_item
    l1_obj.append(l1_abs)
    
    #~ if os.path.isfile(obj_l1):
        #~ obj_l1.append(_)
        #~ print obj_l1
        #~ item_dict['conf'] = obj_l1
    
    
    #~ if os.path.isdir(abspath):
        #~ item_dict[_] = abspath
        
        #~ for _ in os.listdir(abspath):
            #~ print abspath + _


from pprint import pprint
pprint(item_dict)
