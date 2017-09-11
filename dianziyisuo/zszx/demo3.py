# http://it.ckcest.cn:8000/portal.php?mod=view&aid=   HomePage
 
# http://it.ckcest.cn:8000/data/attachment/portal/   PhotoURL
 # -*- coding: utf-8 -*- 

import pymysql
from bs4 import BeautifulSoup

db = pymysql.connect("172.16.155.12","root","myzszx002","zszx2017",charset = "utf8")
cursor = db.cursor()


sql = "select PhotoURL from expert2017_copy"

try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		if(row[0]):
			photourl = "http://it.ckcest.cn:8000/data/attachment/portal/" + row[0]
			print(photourl)
			update_sql = """update expert2017_copy set newPhotoURL = "%s" where PhotoURL = "%s" """%(photourl, row[0])
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