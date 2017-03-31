# -*- coding: utf-8 -*-

from pprint import pprint
import requests
'''abfdb924b7acbab3c97066a27ab34c47'''


def locationPlace(city=u'北京'):
    params = {
        u'key': u'abfdb924b7acbab3c97066a27ab34c47',
        u'city': city,
        u'extensions': u'all', # all or base
        u'output': u'json',
    }
    headers = {
        u'User-Agent': u'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    }
    url = u'http://restapi.amap.com/v3/weather/weatherInfo'
    r = requests.get(url, params=params, headers=headers)
    print r.url
    return r.json()


pprint(locationPlace('厦门'))