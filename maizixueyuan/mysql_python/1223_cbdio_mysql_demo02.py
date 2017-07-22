# coding=utf-8

import pymysql
from bs4 import BeautifulSoup
import requests

# 打开数据库连接
db = pymysql.connect("localhost", "root", "resolution", "TESTDB")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS CBDIO7")


# 使用预处理语句创建表
sql1 = """CREATE TABLE CBDIO7(TITLE CHAR(100) NOT NULL,TIME CHAR(100),CONTENT CHAR(100))default character set utf8"""

try:
    # 执行sql语句
    cursor.execute(sql1)
    # 提交到数据库执行
    db.commit()
except:
    # 如果发生错误则回滚
    db.rollback()


urls = ['http://www.cbdio.com/index_2.html']
        #.format(str(i)) for i in range(2,30)]
for url in urls:
    wb_data = requests.get(url)
    wb_data.encoding = 'utf-8'
    #在这里需要将网页数据的编码改为utf-8，否则可能会出现编码错误
    soup = BeautifulSoup(wb_data.text, 'html.parser')

    titles = soup.select('div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > ul > li > div > p.cb-media-title > a')
    times = soup.select('div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > ul > li > div > p.cb-media-datetime')
    contents = soup.select('div.am-container.cb-main > div.am-g > div.am-u-md-8 > div > ul > li > div > p.cb-media-summary')

    for title,time,content in zip(titles,times,contents):
        
        mytitle1 = title.get_text()
        mytime1 = time.get_text()
        mycontent1 = content.get_text()

        mytitle = mytitle1.encode().decode('utf-8')
        mytime = mytime1.encode().decode('utf-8')
        mycontent = mycontent1.encode().decode('utf-8')
        '''
        mytitle = 'fdsaghraehredgraf'
        mytime = 'fasfdafadsfdasfdasfd'
        mycontent = 'fdsaflashfdsa'
        '''

        sql2 = """INSERT INTO CBDIO7(TITLE,TIME,CONTENT) VALUES ('%s','%s', '%s')"""%(mytitle, mytime, mycontent)
        print(sql2)
        try:
            # 执行sql语句
            cursor.execute(sql2)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
            
        data = [{
            'title':title.get_text(),
            'time':time.get_text(),
            'content':content.get_text(),
            }]
        print(data)
        print(type(title.get_text()))


# 关闭数据库连接
db.close()


