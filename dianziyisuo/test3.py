# coding=utf-8
import requests
#from bs4 import BeautifulSoup as bs

s = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Origin': 'http://www.v2ex.com',
    'Referer': 'http://www.v2ex.com/signin',
    'Host': 'www.v2ex.com',
}

r = s.get('http://www.v2ex.com/signin', headers=headers)


login_data = {'u': 'ArmstrongLLQ', 'p': 'v2exllq921207'}

s.post('http://www.v2ex.com/signin', login_data, headers=headers)

f = s.get('http://www.v2ex.com/settings', headers=headers)
print(f)
print(f.content)