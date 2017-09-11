# -*- coding: utf-8 -*-
import json
import requests
import urllib


BASE_URL = 'http://121.42.164.187:8088/'
AUTH = ('xxjs', '123456a?')
FILTER = {"term_l1":"Technology","year":"2017"}
headers = {
    #'Origin':'http://121.42.164.187:8088',
    #'Referer':'http://121.42.164.187:8088/api-auth/login/?next=/doaj/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.7 Safari/537.36',
    #'Host': '121.42.164.187:8088',
    #'Connection': 'keep-alive',
    #'Cookie':'csrftoken=vnQ1wh7dnCCOlGYmiPV8AwSSoMufK2HN4sptT2ISSadTVmbEpumz1GxHCz9DOUAb'
}
def test_get_doaj_list():
    rsp = requests.get( 'http://121.42.164.187:8088/doaj/?format=json', auth=AUTH, params=FILTER, headers=headers)
    print(rsp)
    if rsp.ok:
        print(rsp.json())

test_get_doaj_list()




