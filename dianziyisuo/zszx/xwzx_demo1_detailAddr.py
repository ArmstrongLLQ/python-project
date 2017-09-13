# -*- coding: utf-8 -*-

import pymysql
from bs4 import BeautifulSoup

db = pymysql.connect("172.16.155.12","root","myzszx002","zszx2017",charset = "utf8")
cursor = db.cursor()


sql = "select id,DetailAddress,test from xwzx2017_copy"

try:
	cursor.execute(sql)
	results = cursor.fetchall()
	i = 0
	for row in results:
		if row[2] == None:
			if(row[1]):
				detail_addr = "http://it.ckcest.cn:8000/portal.php?mod=view&aid=" + row[1]

				update_sql = """update xwzx2017_copy set test = "%s" where id = %d """%(detail_addr, row[0])
				cursor.execute(update_sql)
				i += 1
				if i >= 1000:
					try:
						i = 0
						db.commit()
					except:
						i = 0
						print("error2")
						# raise
						db.rollback()

except:
	print("error1")
	# raise
	db.rollback()

cursor.close()
db.close()


