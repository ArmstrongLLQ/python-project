'''
通过登录和设置filter，爬取数据，并存入数据库
'''
# -*- coding: utf-8 -*-
import json
import requests
import urllib
import codecs
import pymysql

class DOAJ:
    def __init__(self, base_url, auth, filter):
        self.base_url = base_url
        self.auth = auth
        self.filter = filter

    def getBaseUrl(self):
        return self.base_url

    def setBaseUrl(self, new_base_url):
        self.base_url = new_base_url

    def getAuth(self):
        return self.auth

    def setAuth(self, new_auth):
        self.auth = new_auth

    def getFilter(self):
        return self.filter

    def setFilter(self, new_filter):
        self.filter = new_filter

    # 将数据库插入语句封装成函数
    def insertMysql(self, each, db, cursor):
        # sql语句
        sql = """INSERT INTO doaj_data(`id`, `title`, `title_translation`, `abstract`, `abstract_translation`, `year`, `url`, `start_page`, `end_page`, `article_created_date`, `article_last_updated`, `journals_publisher`, `journals_language`, `journals_licenseId`, `journals_title`, `journals_country`, `journals_number`, `journals_volume`, `journals_issns`, `journals_create_date`, `term`, `term_code`, `term_l1`, `keyword`, `keyword_translation`, `author_name`, `author_affiliation`, `author_email`, `identifier_type`, `identifier_identifierId`, `license_type`, `license_title`, `license_url`) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")"""%(each['id'], each['title'], each['title_translation'], each['abstract'], each['abstract_translation'], each['year'], each['url'], each['start_page'], each['end_page'], each['article_created_date'], each['article_last_updated'], each['journals_publisher'], each['journals_language'], each['journals_licenseId'], each['journals_title'], each['journals_country'], each['journals_number'], each['journals_volume'], each['journals_issns'], each['journals_create_date'], each['term'], each['term_code'], each['term_l1'], each['keyword'], each['keyword_translation'], each['author_name'], each['author_affiliation'], each['author_email'], each['identifier_type'], each['identifier_identifierId'], each['license_type'], each['license_title'], each['license_url'])

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print('insert success')
        except Exception:
            # 如果发生错误则回滚
            print('insert fail')
            raise
            db.rollback()

    # 进行数据爬取，并存入数据库
    def insertDoajDatabase(self, my_host, my_username, my_keyword, my_database):
        # 打开数据库连接
        db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        rsp = requests.get(urllib.parse.urljoin(self.base_url, '/doaj/'), auth=self.auth, params=self.filter)
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
                self.insertMysql(each, db, cursor)

        while next_page_url != 'None':
            rsp = requests.get(next_page_url, auth=self.auth,)
            rsp.encoding = 'utf-8'
            next_page_url = str(rsp.json()['next'])
            #print(next_page_url)
            #print(rsp)
            for each in rsp.json()['results']:
                #print(each['id'])
                self.insertMysql(each, db, cursor)

        # 关闭游标
        cursor.close()
        # 关闭连接
        db.close() 

        

if __name__ == '__main__':
    # 在此可以修改用户名、密码以及fileter参数
    base_url = 'http://121.42.164.187:8088/'
    auth = ('xxjs', '123456a?')
    filter = {"term_l1":"Science","year":"2017"}

    # 创建一个对象，可以通过setBaseUrl/setAuth/setFilter方法对参数进行修改
    test1 = DOAJ(base_url, auth, filter)
    test1.insertDoajDatabase("localhost", "root", "", "lilanqing")
