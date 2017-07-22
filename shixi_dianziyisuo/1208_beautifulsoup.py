#coding: utf-8
from bs4 import BeautifulSoup
import requests

url = 'http://www.qiushibaike.com/hot/page/3/?s=4936793'
wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text,'lxml')
userIDs = soup.select('#qiushi_tag_118124456 > a > div')
print userIDs
