# -*- coding: utf-8 -*-

import json
from pprint import pprint
import requests
'''iEOeleQlSwgGA4GelNyIPHu53KYOwElG'''


def locatePlace(address, city=None):
    params = {
        u'output': u'json',
        u'ak': u'iEOeleQlSwgGA4GelNyIPHu53KYOwElG',
        #~ u'ret_coordtype	': u'gcj02ll / bd09mc',
        #~ u'callback': u'showLocation / renderOption',
        u'address': address,
        u'city': city,
    }
    headers = {
        u'User-Agent': u'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    }
    url = u'http://api.map.baidu.com/geocoder/v2/'
    r = requests.get(url, params=params, headers=headers)
    r = r.json()
    return r


print locatePlace(u'望京')