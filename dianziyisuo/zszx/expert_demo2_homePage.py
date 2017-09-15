# -*- coding: utf-8 -*-

import pymysql
from bs4 import BeautifulSoup

db = pymysql.connect("172.16.155.12","root","myzszx002","zszx2017",charset = "utf8")
cursor = db.cursor()


sql = "select HomePage from expert2017_copy"

try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		homepage = "http://it.ckcest.cn:8000/portal.php?mod=view&aid=" + row[0]
		print(homepage)
		update_sql = """update expert2017_copy set newHomePage = "%s" where HomePage = "%s" """%(homepage, row[0])
		try:
			cursor.execute(update_sql)
			db.commit()
		except:
			print("error",)
			db.rollback()

except:
	print("error")
	db.rollback()

cursor.close()
db.close()