# -*- coding: utf-8 -*-
import json
import requests
import urllib


BASE_URL = 'http://121.42.164.187:8088/'
AUTH = ('xxjs', '123456a?')
FILTER = {"term_l1": "Technology", "year" : "2017"}

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.7 Safari/537.36',
    'Host':'121.42.164.187:8088',
    'Connection':'keep-alive',
}

login_url = 'http://121.42.164.187:8088/api-auth/login/'
username = 'xxjs'
password = '123456a?'
url = BASE_URL + '/doaj/?format=json'
s = requests.Session()  # 可以在多次访问中保留cookie
s.post(login_url, {'username':username, 'password': password}, headers=headers)  # POST帐号和密码，设置headers
r = s.get(url)  # 已经是登录状态了
print(r)

'''
def test_get_doaj_list(self):
    rsp = requests.get(BASE_URL, headers=headers)
    print(rsp)
    if rsp.ok:
        print(rsp.json())
'''
