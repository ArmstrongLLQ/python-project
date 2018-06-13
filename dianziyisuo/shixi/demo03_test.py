#coding: utf-8
'''
使用beautifulsoup爬取www.cbdio.com的新闻数据，包括标题（title），时间（time），
##内容简介（content），并将抓取到的内容转化为json格式存储
'''
from bs4 import BeautifulSoup
import requests
import json
import io


a = '123456'

b = a[:3]

print(b)