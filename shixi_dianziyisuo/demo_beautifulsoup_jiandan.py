from bs4 import BeautifulSoup
import requests

import re
import os


os.mkdir('jiandan2')
os.chdir('jiandan2')
urls = ['http://jandan.net/ooxx/page-{}#comments'.format(str(i)) for i in range(2252, 2262)]
for url in urls:
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    img_urls = soup.select('div.text > p > img')
    for img_url in img_urls:
        print(img_url.get('src'))
#    for each in img_urls:
#        with open(, 'wb') as f:
#            img_req = requests.get(each.get('src'), stream=True)
#            for chunk in img_req:
#                f.write(chunk)  
#print(img_urls)

