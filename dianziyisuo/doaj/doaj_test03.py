# coding=utf-8
import requests
#from bs4 import BeautifulSoup as bs

s = requests.Session()
headers = {
    'Origin':'http://121.42.164.187:8088',
    'Referer':'http://121.42.164.187:8088/api-auth/login/?next=/doaj/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.7 Safari/537.36',
    'Host': '121.42.164.187:8088',
    'Connection': 'keep-alive',
    #'Cookie':'csrftoken=vnQ1wh7dnCCOlGYmiPV8AwSSoMufK2HN4sptT2ISSadTVmbEpumz1GxHCz9DOUAb'
}

r = s.get('http://121.42.164.187:8088/api-auth/login/?next=/', headers=headers)
print(r.cookies)

login_data = {'u': 'xxjs', 'p': '123456a?'}

a = s.post('http://121.42.164.187:8088/api-auth/login/?next=/', login_data, headers=headers)
print(a)

f = s.get('http://121.42.164.187:8088/doaj/', headers=headers)
print(f)
print(f.content)