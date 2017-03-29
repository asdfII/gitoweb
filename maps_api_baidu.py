# -*- coding: cp936 -*-

import requests
'''abfdb924b7acbab3c97066a27ab34c47'''
'''iEOeleQlSwgGA4GelNyIPHu53KYOwElG'''


def locatebyAddr(address, city=None):
    items = {
        'output': 'json',
        'ak': 'iEOeleQlSwgGA4GelNyIPHu53KYOwElG',
        'address': address
    }
    if city:
        items['city'] = city
    r = requests.get('http://api.map.baidu.com/geocoder/v2/', params=items)
    dictResult = r.json()
    return dictResult['result']['location'] if not dictResult['status'] else None


def locatebyLatLon(lat, lon, pois=0):
    items = {'location': str(lat) + ',' + str(lon), 'ak': 'iEOeleQlSwgGA4GelNyIPHu53KYOwElG', 'output': 'json'}
    if pois:
        items['pois'] = 1
    r = requests.get('http://api.map.baidu.com/geocoder/v2/', params=items)
    dictResult = r.json()
    return dictResult['result'] if not dictResult['status'] else None


def main():
    address = raw_input('Enter your address: ')
    city = raw_input('Enter your city(optional): ')
    result = locatebyAddr(address, city)
    print(result)


if __name__ == '__main__':
    main()