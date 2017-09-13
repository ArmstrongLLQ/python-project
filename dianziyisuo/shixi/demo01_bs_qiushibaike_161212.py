from bs4 import BeautifulSoup
import requests
import json

#coding: utf-8

urls = ['http://www.qiushibaike.com/8hr/page/{}/?s=4938422'.format(str(i)) for i in range(2, 10)]
for url in urls:
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'html.parser')
    contents = soup.select('div.content > span')
    names = soup.select('div.author.clearfix > a')
    for content,name in zip(contents, names):
        data = [{
            'content': content.get_text(),
            'name': name.get('title')
            }]
        '''
        print(data)

        '''
        with open('qiushibaike.json', 'a') as json_file:
            json_file.write(json.dumps(data,separators=(',',':'), ensure_ascii=False))
            json_file.write('\n')
        
