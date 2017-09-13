#coding: utf-8
'''
使用beautifulsoup爬取www.cbdio.com的新闻数据，包括标题（title），时间（time），
##内容简介（content），并将抓取到的内容转化为json格式存储
'''
from bs4 import BeautifulSoup
import requests
import json
import io

urls = ['http://www.cbdio.com/index_{}.html'.format(str(i)) for i in range(2,30)]
for url in urls:
    wb_data = requests.get(url)
    wb_data.encoding = 'utf-8'
    #在这里需要将网页数据的编码改为utf-8，否则可能会出现编码错误
    soup = BeautifulSoup(wb_data.text, 'html.parser')

    titles = soup.select('div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > ul > li > div > p.cb-media-title > a')
    times = soup.select('div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > ul > li > div > p.cb-media-datetime')
    contents = soup.select('div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > ul > li > div > p.cb-media-summary')

    for title,time,content in zip(titles,times,contents):
        data = [{
            'title':title.get_text(),
            'time':time.get_text(),
            'content':content.get_text(),
            }]
        print(type(title.get_text()))
