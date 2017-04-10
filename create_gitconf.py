# -*- coding: utf-8 -*-

import ConfigParser


with open('gitolite.conf', 'rb') as file:
    fp = open('new.conf', 'ab+')
    for line in file.readlines():
        #~ line = line.rstrip('\n')
        fp.write(line)
    fp.write('\n')
    fp.close()