# -*- coding: utf-8 -*-

import pymysql
from bs4 import BeautifulSoup

db = pymysql.connect("172.16.155.92","root","myzszx002","zszx2017",charset = "utf8", port=3326)
cursor = db.cursor()


sql = "select DetailAddress from cyzc2017_copy"

try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		if(row[0]):
			detail_addr = "http://it.ckcest.cn/portal.php?mod=view&aid=" + row[0]

			update_sql = """update cyzc2017_copy set newDetailAddress = "%s" where DetailAddress = "%s" """%(detail_addr, row[0])
			try:
				cursor.execute(update_sql)
				db.commit()
			except:
				print("error2")
				db.rollback()

except:
	print("error1")
	raise
	db.rollback()

cursor.close()
db.close()


