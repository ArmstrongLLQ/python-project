# -*- coding: utf-8 -*-
import pymysql
from bs4 import BeautifulSoup

db = pymysql.connect("172.16.155.12","root","myzszx002","zszx2017",charset = "utf8")
cursor = db.cursor()


sql = "select id,Introduction from expert2017_copy"

try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        if row[1] != None:
            soup = BeautifulSoup(row[1], 'lxml')
            new_introduction = ""
            for para in soup.find_all():
                new_introduction += para.get_text()
            new_introduction = new_introduction.replace("'", "\\'")
            new_introduction = new_introduction.replace('"', '\\"')
            update_sql = """update expert2017_copy set newIntroduction = "%s" where id = %d """%(new_introduction, row[0])
            try:
                cursor.execute(update_sql)
                db.commit()
            except:
                print("error1")
                db.rollback()
            print('\n')

except:
    print("error2")
    db.rollback()
cursor.close()
db.close()

