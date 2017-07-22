from bs4 import BeautifulSoup
import requests
#-*- coding:utf-8 -*-

url = 'http://www.qiushibaike.com/hot/'
wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text, 'lxml')
contents = soup.select('div.content > span')
names = soup.select('div.author.clearfix > a > h2')

for content,name in zip(contents,names):
    mycontent = content.encode('utf-8')
    myname = name.encode('utf-8')

    #print('content:%s'%mycontent)
    
    data = {
        'content:' : mycontent,
        'name' : myname,
        }
    print(data)
    
'''
urls = ['http://jandan.net/ooxx/page-{}#comments'.format(str(i)) for i in range(2252, 2262)]
for url in urls:
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    img_urls = soup.select('div.text > p > img')
    for img_url in img_urls:
        print(img_url.get('src'))
    for each in img_urls:
        with open(, 'wb') as f:
            img_req = requests.get(each.get('src'), stream=True)
            for chunk in img_req:
                f.write(chunk)
'''
