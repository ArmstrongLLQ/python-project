# coding=utf-8
'''
功能：使用BeautifulSoup爬取网页（二级），然后将爬取的相关内容存入数据库
版本：v3.0
时间：2017-01-05
作者：李岚清
备注：新版本加入了uuid模块，用来生成每个数据的GUID
'''
import pymysql
from bs4 import BeautifulSoup
import requests
import uuid

class CBDIO:
    def __init__(self):
        pass
    
    #通过url获取网页数据
    def GetPage(self, url):
        wb_data = requests.get(url)
            
        #在这里需要将网页数据的编码改为utf-8，否则可能会出现编码错误
        wb_data.encoding = 'utf-8'
            
        soup = BeautifulSoup(wb_data.text, 'html.parser')        
        return soup
    
    #执行数据库语句操作
    def DoMysql(self, sql, db):
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            print('yes')
            db.commit()
        except:
            # 出错的话就回滚
            print('no')
            db.rollback()          
    
    #爬取一级和二级页面的数据，存入数据库
    def SpideDataToMysql(self, soup, db):
        #一级页面需要获取的数据‘标题’、‘时间’、‘简介’
        titles = soup.select('div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > ul > li > div > p.cb-media-title > a')
        times = soup.select('div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > ul > li > div > p.cb-media-datetime')
        descriptions = soup.select('div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > ul > li > div > p.cb-media-summary')
        
        #从一级页面获取二级页面的url，存入列表second_url  
        content_urls = soup.select('body > div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > ul > li > div > p.cb-media-title > a')
        second_urls = []
        for each in content_urls:
            second_urls.append('http://www.cbdio.com/'+each.get('href'))
        
        #将一级页面获取的数据变为字典，然后将数据存入数据库     
        for title,time,description,second_url in zip(titles,times,descriptions,second_urls):
            guid = uuid.uuid3(uuid.NAMESPACE_DNS, second_url)
            data = {
                'title':title.get_text(),
                'time':time.get_text(),
                'description':description.get_text(),
                'guid':guid,
                'detailaddress':second_url,
            }
            
            # SQL 插入语句 插入GUID, DatasetID, Title, PublishTime, DetailWebsite, DetailAddress, Abstract, Description
            sql = "INSERT INTO info_newsinfo(GUID, DatasetID, Title, PublishTime, DetailWebsite, DetailAddress, Abstract, Description) \
            VALUES ('%s', 'N1', '%s', '%s', '数据观', '%s', '%s', '%s')" % (data['guid'], data['title'], data['time'], data['detailaddress'], data['description'], data['description'])
            #将data存入数据库
            self.DoMysql(sql, db)
            
            #开始爬取二级页面的数据，由于每一个一级页面的标题对应一个二级页面，故需要二级循环
            second_soup = self.GetPage(second_url)
            second_titles = second_soup.select('body > div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > h1')
            
            #爬取二级页面的数据‘作者’、‘来源’、‘详细内容’
            for second_title in second_titles:
                second_contents = second_soup.select('body > div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > p')
                authors = second_soup.select('body > div.am-container.cb-main > div.am-g > div.am-u-md-8 > div:nth-of-type(1) > p.cb-article-info > span:nth-of-type(3)')
                sources = second_soup.select('body > div.am-container.cb-main > div.am-g > div.am-u-md-8 > div:nth-of-type(1) > p.cb-article-info > span:nth-of-type(1)')
            
                #将详细内容存入数据库
                #详细内容由多个部分组成，需要先组合成一个字符串存储
                content_data = []
                for second_content in second_contents:
                    content_data.append(second_content.get_text())
                content_data_str = ' '.join(content_data)    
                
                #存入字典data
                data['maintext'] = content_data_str      
                
                # SQL 更新语句
                sql = "UPDATE info_newsinfo SET MainText = '%s' WHERE Title = '%s'" % (data['maintext'], data['title'])
                self.DoMysql(sql, db)
                
                #将‘作者’存入数据库
                for author in authors:
                    data['author'] = author.get_text()
                    sql = "UPDATE info_newsinfo SET Author = '%s' WHERE Title = '%s'" % (data['author'], data['title'])
                    self.DoMysql(sql, db)
                
                #将‘来源’存入数据库
                for source in sources:
                    data['source'] = source.get_text()
                    sql = "UPDATE info_newsinfo SET Source = '%s' WHERE Title = '%s'" % (data['source'], data['title'])
                    self.DoMysql(sql, db)
    
    def Start(self):
        #连接数据库
        db = pymysql.connect("172.16.1.139","devdemo","devdemo","devdemo",charset='utf8')
        #爬取的网址
        urls = ['http://www.cbdio.com/index_{}.html'.format(str(i)) for i in range(2,30)]
        for url in urls:
            page_soup = self.GetPage(url)
            self.SpideDataToMysql(page_soup, db)
        
        #关闭数据库
        db.close()
            
            
test = CBDIO()
test.Start()

