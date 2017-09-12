# -*- coding: utf-8 -*- 
# 性别0男1女

import pymysql
from bs4 import BeautifulSoup

db = pymysql.connect("172.16.155.12","root","myzszx002","zszx2017",charset = "utf8")
cursor = db.cursor()


sql = "select id,Sex from expert2017_copy"

try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		if row[1]==0:
			update_sql = """update expert2017_copy set gender = "%s" where id = %d """%('男', row[0])
		else:
			update_sql = """update expert2017_copy set gender = "%s" where id = %d """%('女', row[0])
	
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
