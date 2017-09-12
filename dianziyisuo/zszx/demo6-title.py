# -*- coding: utf-8 -*- 
# 职称 0未选、1院士、2正高、3副高、4中级、5初级、9其他

import pymysql
from bs4 import BeautifulSoup

db = pymysql.connect("172.16.155.12", "root", "myzszx002", "zszx2017", charset="utf8")
cursor = db.cursor()


sql = "select id,Title from expert2017_copy"

try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        if row[1]==0:
            update_sql = """update expert2017_copy set newTitle = "%s" where id = %d """%('Others', row[0])
        elif row[1]==1:
            update_sql = """update expert2017_copy set newTitle = "%s" where id = %d """%('Academician', row[0])
        elif row[1]==2:
            update_sql = """update expert2017_copy set newTitle = "%s" where id = %d """%('SeniorTitle', row[0])
        elif row[1]==3:
            update_sql = """update expert2017_copy set newTitle = "%s" where id = %d """%('SeniorTitle', row[0])
        elif row[1] == 4:
            update_sql = """update expert2017_copy set newTitle = "%s" where id = %d """%('IntermediateTitle', row[0])
        elif row[1]==5:
            update_sql = """update expert2017_copy set newTitle = "%s" where id = %d """%('PrimaryTitle', row[0])
        else:
            update_sql = """update expert2017_copy set newTitle = "%s" where id = %d """%('Others', row[0])


        try:
            cursor.execute(update_sql)
            db.commit()
        except:
            print("error")
            db.rollback()

except:
    print("error")

    db.rollback()

cursor.close()
db.close()
