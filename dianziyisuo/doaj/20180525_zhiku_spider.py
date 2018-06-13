# -*- coding: utf-8 -*-
'''
通过登录和设置filter，
爬取数据，并存入数据库
对数据库数据进行增删改查操作
'''

import json
import requests
import urllib
import pymysql

class DOAJ:
    def __init__(self, base_url, auth):
        self.__base_url = base_url
        self.__auth = auth

    def getBaseUrl(self):
        return self.__base_url

    def setBaseUrl(self, new_base_url):
        self.__base_url = new_base_url

    def getAuth(self):
        return self.__auth

    def setAuth(self, new_auth):
        self.__auth = new_auth


    def __connectDatabase(self, my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
        # 打开数据库连接
        db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        return db, cursor

    # 将数据库插入语句封装成函数
    def __insertMysql(self, each, db, cursor):
        # sql语句
        sql = """INSERT INTO zhiku_data_copy(`id`,`title` ,`title_alternative`,`publish_date`,`domain`,`topic`,`category`,
`module`,`language`,`content`,`html_content`,`abstract`,`keywords`,`reference`,`author`,`url`,`image_url`,`keywords_alternative`,
`abstract_alternative`,`topic_l1`,`related_topic`,`file_url`,`projects`,`geography`,`license_url`,`oss_url`) VALUES 
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        my_value = (each['id'], each['title'], each['title_alternative'], each['publish_date'], each['domain'],
                    each['topic'], each['category'], each['module'], each['language'], each['content'],
                    each['html_content'], each['abstract'], each['keywords'],
                    each['reference'], each['author'], each['url'], each['image_url'],
                    each['keywords_alternative'], each['abstract_alternative'], each['topic_l1'], each['related_topic'],
                    each['file_url'], each['projects'], each['geography'], each['license_url'], each['oss_url'])
        try:
            # 执行sql语句
            cursor.execute(sql, my_value)
            # 提交到数据库执行
            db.commit()

        except Exception as e:
            # 如果发生错误则回滚
            print(e)
            # raise
            db.rollback()

    # 进行数据爬取，并存入数据库
    def insertDoajDatabase(self, my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
        db, cursor = self.__connectDatabase(my_host, my_username, my_keyword, my_database)

        # 获取网页数据
        rsp = requests.get(self.__base_url, auth=self.__auth)
        rsp.encoding = 'utf-8'

        # 得到下一页要爬取数据的url
        next_page_url = str(rsp.json()['next'])
        # 将当前页面的数据存入数据库
        if rsp.ok:
            for each in rsp.json()['results']:
                #print(each['id'])
                self.__insertMysql(each, db, cursor)

        while next_page_url != 'None':
            rsp = requests.get(next_page_url, auth=self.__auth)
            rsp.encoding = 'utf-8'
            next_page_url = str(rsp.json()['next'])
            #print(next_page_url)
            #print(rsp)
            for each in rsp.json()['results']:
                self.__insertMysql(each, db, cursor)

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

if __name__ == '__main__':
    # 在此可以修改用户名、密码以及fileter参数
    base_url = 'http://121.42.164.187:8088/zhiku_api/details/'
    auth = ('xxjs', '123456a?')


    test1 = DOAJ(base_url, auth)
    test1.insertDoajDatabase("172.16.155.11", "doaj", "Doa123!@#j", "doaj")

    # 创建一个对象，可以通过setBaseUrl/setAuth/setFilter方法对参数进行修改


    #test1.selectFromDatabase('select * from doaj_data')
    #test1.updateDatabase('update doaj_data set title = "test title" where id = 54')
    #test1.deleteDatabase('delete from doaj_data where id = 21')
