# -*- coding: utf-8 -*-

import ConfigParser

from gitoweb.settings import BASE_DIR


with open(BASE_DIR + '/conf/gitolite.conf', 'rb') as file:
    fp = open(BASE_DIR + '/new.conf', 'ab+')
    for line in file.readlines():
        #~ line = line.rstrip('\n')
        fp.write(line)
    fp.close()
