from bs4 import BeautifulSoup
import requests

#coding: utf-8

url = 'http://www.cbdio.com/'
wb_data = requests.get(url)
wb_data.encoding = 'utf-8'
soup = BeautifulSoup(wb_data.text, 'html.parser')
titles = soup.select('div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > ul > li > div > p.cb-media-title > a')
times = soup.select('div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > ul > li > div > p.cb-media-datetime')
contents = soup.select('div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > ul > li > div > p.cb-media-summary')
for title,time,content in zip(titles,times,contents):
    '''
    file.write(title.get_text())
    file.write(time.get_text())
    file.write(content.get_text())
    '''

    data = {
        'title:':title.get_text(),
        'time:':time.get_text(),
        'content:':content.get_text(),
        }
    print(data)
