'''
通过登录和设置filter，
爬取数据，并存入数据库
对数据库数据进行增删改查操作
'''
# -*- coding: utf-8 -*-
import json
import requests
import urllib
import pymysql
import threading
import queue

class DOAJ:
    def __init__(self, base_url, auth, new_filter):
        self.__base_url = base_url
        self.__auth = auth
        self.__filter = new_filter

    def getBaseUrl(self):
        return self.__base_url

    def setBaseUrl(self, new_base_url):
        self.__base_url = new_base_url

    def getAuth(self):
        return self.__auth

    def setAuth(self, new_auth):
        self.__auth = new_auth

    def getFilter(self):
        return self.__filter

    def setFilter(self, new_filter):
        self.__filter = new_filter

    def __connectDatabase(self, my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
        # 打开数据库连接
        db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        return db, cursor

    # 将数据库插入语句封装成函数
    def __insertMysql(self, each, db, cursor, insert_success):
        # sql语句
        sql = """INSERT INTO doaj_data(`id`, `title`, `title_translation`, `abstract`, `abstract_translation`, `year`, `url`, `start_page`, `end_page`, `article_created_date`, `article_last_updated`, `journals_publisher`, `journals_language`, `journals_licenseId`, `journals_title`, `journals_country`, `journals_number`, `journals_volume`, `journals_issns`, `journals_create_date`, `term`, `term_code`, `term_l1`, `keyword`, `keyword_translation`, `author_name`, `author_affiliation`, `author_email`, `identifier_type`, `identifier_identifierId`, `license_type`, `license_title`, `license_url`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        my_value = (each['id'], each['title'], each['title_translation'], each['abstract'], each['abstract_translation'], each['year'], each['url'], each['start_page'], each['end_page'], each['article_created_date'], each['article_last_updated'], each['journals_publisher'], each['journals_language'], each['journals_licenseId'], each['journals_title'], each['journals_country'], each['journals_number'], each['journals_volume'], each['journals_issns'], each['journals_create_date'], each['term'], each['term_code'], each['term_l1'], each['keyword'], each['keyword_translation'], each['author_name'], each['author_affiliation'], each['author_email'], each['identifier_type'], each['identifier_identifierId'], each['license_type'], each['license_title'], each['license_url'])
        try:
            # 执行sql语句
            cursor.execute(sql, my_value)
            # 提交到数据库执行
            db.commit()
            insert_success += 0
            print('insert success')
        except Exception:
            # 如果发生错误则回滚
            print('insert fail')
            # raise
            insert_success += 1
            db.rollback()

        return insert_success

    # 进行数据爬取，并存入数据库
    def insertDoajDatabase(self, my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
        db, cursor = self.__connectDatabase(my_host, my_username, my_keyword, my_database)

        # 获取网页数据
        rsp = requests.get(urllib.parse.urljoin(self.__base_url, '/doaj/'), auth=self.__auth, params=self.__filter)
        rsp.encoding = 'utf-8'

        # 得到下一页要爬取数据的url
        next_page_url = str(rsp.json()['next'])
        #pre_page_url = str(rsp.json()['previous'])
        #print(next_page_url)
        #print(pre_page_url)
        insert_success = 0
        # 将当前页面的数据存入数据库
        if rsp.ok:
            for each in rsp.json()['results']:
                #print(each['id'])
                self.__insertMysql(each, db, cursor, insert_success)

        while next_page_url != 'None':
            rsp = requests.get(next_page_url, auth=self.__auth)
            rsp.encoding = 'utf-8'
            next_page_url = str(rsp.json()['next'])
            #print(next_page_url)
            #print(rsp)
            for each in rsp.json()['results']:
                self.__insertMysql(each, db, cursor, insert_success)

        # 关闭数据库连接
        cursor.close()
        db.close()

    def insertNewData(self, my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
        db, cursor = self.__connectDatabase(my_host, my_username, my_keyword, my_database)
        insert_success = 0
        # 获取网页数据
        rsp = requests.get(urllib.parse.urljoin(self.__base_url, '/doaj/'), auth=self.__auth, params=self.__filter)
        rsp.encoding = 'utf-8'
        data_count = int(str(rsp.json()['count']))
        last_page = data_count // 20 + 1
        last_page_url = "http://121.42.164.187:8088/doaj/?page=%s&term_l1=%s&year=%s" % (last_page, self.__filter['term_l1'], self.__filter['year'])
        rsp = requests.get(last_page_url, auth=self.__auth)
        rsp.encoding = 'utf-8'
        
        if rsp.ok:
            for each in rsp.json()['results']:
                insert_success = self.__insertMysql(each, db, cursor, insert_success)

        while insert_success == 0:
            last_page -= 1
            last_page_url = "http://121.42.164.187:8088/doaj/?page=%s&term_l1=%s&year=%s" % (last_page, self.__filter['term_l1'], self.__filter['year'])
            rsp = requests.get(last_page_url, auth=self.__auth)
            rsp.encoding = 'utf-8'
            for each in rsp.json()['results']:
                insert_success = self.__insertMysql(each, db, cursor, insert_success)

        # 关闭数据库连接
        cursor.close()
        db.close()


    # 数据库查询操作，传入查询语句和数据库信息（默认）
    def selectFromDatabase(self, select_sql, my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
        # 打开数据库连接 "172.16.155.11", "doaj", "Doa123!@#j", "doaj"
        db, cursor = self.__connectDatabase(my_host, my_username, my_keyword, my_database)
     
        sql = select_sql
        try:
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                print(row)
                print('\n')

        except :
            print('Error: unable to fetch data.')

        # 关闭数据库连接
        cursor.close()
        db.close() 

    # 更新数据库
    def updateDatabase(self, update_sql, my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
        # 打开数据库连接 "172.16.155.11", "doaj", "Doa123!@#j", "doaj"
        db, cursor = self.__connectDatabase(my_host, my_username, my_keyword, my_database)

        sql = update_sql

        try:
            cursor.execute(sql)
            db.commit()
            print('update success.\n')

        except :
            print('Error: unable to update data.')
            db.rollback()

        # 关闭数据库连接
        cursor.close()
        db.close() 

    # 删除数据
    def deleteDatabase(self, delete_sql, my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
        # 打开数据库连接 "172.16.155.11", "doaj", "Doa123!@#j", "doaj"
        db, cursor = self.__connectDatabase(my_host, my_username, my_keyword, my_database)
        
        sql = delete_sql

        try:
            cursor.execute(sql)
            db.commit()
            print('delete success.\n')

        except :
            # 如果发生错误则回滚
            print('Error: unable to delete data.')
            db.rollback()

        # 关闭数据库连接
        cursor.close()
        db.close()
        
    def getCount(self):
        # 获取网页数据
        rsp = requests.get(urllib.parse.urljoin(self.__base_url, '/doaj/'), auth=self.__auth, params=self.__filter)
        rsp.encoding = 'utf-8'
        # 得到下一页要爬取数据的url
        term_count = str(rsp.json()['count'])

        return term_count      

class CrawlThread(threading.Thread):
    def __init__(self, filter_queue):
        threading.Thread.__init__(self)
        self.filter_queue = filter_queue

    def run(self):
        while True:
            print('thread start----------------------------------')
            if self.filter_queue.empty():
                print('thread end-------------------------------------')
                break
            filter1 = self.filter_queue.get()
            test1 = DOAJ('http://121.42.164.187:8088/', ('xxjs', '123456a?'), filter1)
            test1.insertNewData("172.16.155.11", "doaj", "Doa123!@#j", "doaj")
            print('thread end-------------------------------------')
            self.filter_queue.task_done()

            
if __name__ == '__main__':
    filter_queue = queue.Queue()
    # 在此可以修改用户名、密码以及fileter参数
    base_url = 'http://121.42.164.187:8088/'
    auth = ('xxjs', '123456a?')
    term_l1 = ['Science', 'Technology', 'Military Science']
    year = ['2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000']
    
    
    for term in term_l1:
        for ayear in year:
            new_filter = {'term_l1':term, 'year':ayear}
            filter_queue.put(new_filter)

    for i in range(10): 
        thread = CrawlThread(filter_queue)
        thread.start()

    filter_queue.join()

    for i in range(10):
        thread.join()

    print('MainThread End')



    # 创建一个对象，可以通过setBaseUrl/setAuth/setFilter方法对参数进行修改
    
    
    #test1.selectFromDatabase('select * from doaj_data')
    #test1.updateDatabase('update doaj_data set title = "test title" where id = 54')
    #test1.deleteDatabase('delete from doaj_data where id = 21')
