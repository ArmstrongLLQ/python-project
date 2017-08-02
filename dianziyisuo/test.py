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
    def __insertMysql(self, each, db, cursor):
        # sql语句
        sql = """INSERT INTO doaj_data(`id`, `title`, `title_translation`, `abstract`, `abstract_translation`, `year`, `url`, `start_page`, `end_page`, `article_created_date`, `article_last_updated`, `journals_publisher`, `journals_language`, `journals_licenseId`, `journals_title`, `journals_country`, `journals_number`, `journals_volume`, `journals_issns`, `journals_create_date`, `term`, `term_code`, `term_l1`, `keyword`, `keyword_translation`, `author_name`, `author_affiliation`, `author_email`, `identifier_type`, `identifier_identifierId`, `license_type`, `license_title`, `license_url`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        my_value = (each['id'], each['title'], each['title_translation'], each['abstract'], each['abstract_translation'], each['year'], each['url'], each['start_page'], each['end_page'], each['article_created_date'], each['article_last_updated'], each['journals_publisher'], each['journals_language'], each['journals_licenseId'], each['journals_title'], each['journals_country'], each['journals_number'], each['journals_volume'], each['journals_issns'], each['journals_create_date'], each['term'], each['term_code'], each['term_l1'], each['keyword'], each['keyword_translation'], each['author_name'], each['author_affiliation'], each['author_email'], each['identifier_type'], each['identifier_identifierId'], each['license_type'], each['license_title'], each['license_url'])
        try:
            # 执行sql语句
            cursor.execute(sql, my_value)
            # 提交到数据库执行
            db.commit()
            print('insert success')
        except Exception:
            # 如果发生错误则回滚
            print('insert fail')
            raise
            db.rollback()

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
        # 将当前页面的数据存入数据库
        if rsp.ok:
            for each in rsp.json()['results']:
                #print(each['id'])
                self.__insertMysql(each, db, cursor)

        while next_page_url != 'None':
            rsp = requests.get(next_page_url, auth=self.__auth,)
            rsp.encoding = 'utf-8'
            next_page_url = str(rsp.json()['next'])
            #print(next_page_url)
            #print(rsp)
            for each in rsp.json()['results']:
                #print(each['id'])
                self.__insertMysql(each, db, cursor)

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


if __name__ == '__main__':
    # 在此可以修改用户名、密码以及fileter参数
    base_url = 'http://121.42.164.187:8088/'
    auth = ('xxjs', '123456a?')
    term_l1 = ['Science', 'Technology', 'Military Science']
    year = ['2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000']
    
    count_sum = 0
    for term in term_l1:
        for ayear in year:
            new_filter = {'term_l1':term, 'year':ayear}
            test1 = DOAJ(base_url, auth, new_filter)
            tmp_count = int(test1.getCount())
            count_sum += tmp_count
            print(count_sum)

    print(count_sum)


 