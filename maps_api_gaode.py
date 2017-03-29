# -*- coding: utf-8 -*-

import requests
from pprint import pprint


city = u'suzhou'
key = u'abfdb924b7acbab3c97066a27ab34c47'
extensions = 'all' # all or base
url = u'http://restapi.amap.com/v3/weather/weatherInfo?city=' + city + u'&key=' + key + u'&extensions=' + extensions
#~ parameters = {
    #~ u'key': u'abfdb924b7acbab3c97066a27ab34c47',
    #~ u'city': u'beijing',
    #~ u'extensions': u'all',
    #~ u'output': u'json',
#~ }
#~ url = u'http://restapi.amap.com/v3/weather/weatherInfo'
r = requests.get(url)
pprint(r.json())