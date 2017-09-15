# -*- coding: utf-8 -*-

import pymysql
from bs4 import BeautifulSoup

db = pymysql.connect("172.16.155.12","root","myzszx002","zszx2017",charset = "utf8")
cursor = db.cursor()


sql = "select id,DetailAddress,newDetailAddress from baike2017_copy"

try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		if row[2] == None:
			if(row[1]):
				detail_addr = "http://it.ckcest.cn:8000/portal.php?mod=view&aid=" + row[1]
				update_sql = """update baike2017_copy set newDetailAddress = "%s" where id = %d """%(detail_addr, row[0])

				try:
					cursor.execute(update_sql)
					db.commit()
				except:

					print("error2")
					raise
					db.rollback()

except:
	print("error1")
	# raise
	db.rollback()

cursor.close()
db.close()


