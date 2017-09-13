#coding: utf-8
'''
使用beautifulsoup爬取www.cbdio.com的新闻数据（1-29页），并且进行了二级页面的爬取，
并将抓取到的内容转化为json格式存储
'''

from bs4 import BeautifulSoup
import requests
import json
import io

urls = ['http://www.cbdio.com/index_{}.html'.format(str(i)) for i in range(1,30)]
for url in urls:
    url = 'http://www.cbdio.com/'
    wb_data = requests.get(url)
    wb_data.encoding = 'utf-8'
    #在这里需要将网页数据的编码改为utf-8，否则可能会出现编码错误
    soup = BeautifulSoup(wb_data.text, 'html.parser')

    content_urls = soup.select('body > div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > ul > li > div > p.cb-media-title > a')
    #获取二级页面的url，存入列表second_url
    second_urls = []
    for each in content_urls:
        second_urls.append('http://www.cbdio.com/'+each.get('href'))

    for each in second_urls:
        second_wb_data = requests.get(each)
        second_wb_data.encoding = 'utf-8'
        second_soup = BeautifulSoup(second_wb_data.text, 'html.parser')

        second_titles = second_soup.select('body > div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > h1')

        for second_title in second_titles:
            second_contents = second_soup.select('body > div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > p')
            content_data = []
            for second_content in second_contents:
                content_data.append(second_content.get_text())
            content_data_str = ' '.join(content_data)
            data = [{
                'title:':second_title.get_text(),
                'content:':content_data_str,
                }]

            with open('data2.json', 'a') as json_file:
                #在打开文件的时候需要将文件的打开方式设置为utf-8，否则会出错
                #UnicodeEncodeError: 'gbk' codec can't encode character '\xa0'
                json_file.write(json.dumps(data, separators=(',',':'), ensure_ascii=False))
                json_file.write('\n')


