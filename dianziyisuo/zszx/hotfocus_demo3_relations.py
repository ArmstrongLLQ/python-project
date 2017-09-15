# -*- coding: utf-8 -*-
import pymysql
from bs4 import BeautifulSoup

db = pymysql.connect("172.16.155.12","root","myzszx002","zszx2017",charset = "utf8")
cursor = db.cursor()


sql = "select id,Relations,newRelations from hotfocus2017_copy"

try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		if row[2] == None:
			soup = BeautifulSoup(row[1], 'lxml')

			new_content = soup.get_text()

			new_content = new_content.replace("'", "\\'")
			new_content = new_content.replace('"', '\\"')

			update_sql = """update hotfocus2017_copy set newRelations = '%s' where id = %d """%(new_content, row[0])
			try:
				cursor.execute(update_sql)
				db.commit()
			except:
				print("error1")
				print(row[0])
				raise
				print('\n')

except:
	print("error2")
	raise
	db.rollback()
cursor.close()
db.close()