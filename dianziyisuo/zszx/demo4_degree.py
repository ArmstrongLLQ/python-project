# -*- coding: utf-8 -*- 
# '学历 0未选、2博士研究生、3硕士研究生、4本科、5大专、6中专、9其他'

import pymysql
from bs4 import BeautifulSoup

db = pymysql.connect("172.16.155.12","root","myzszx002","zszx2017",charset = "utf8")
cursor = db.cursor()


sql = "select id,Degree from expert2017_copy"

try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		if row[1]==0:
			update_sql = """update expert2017_copy set newDegree = "%s" where id = %d """%('其他', row[0])
		elif row[1]==2:
			update_sql = """update expert2017_copy set newDegree = "%s" where id = %d """%('Doctor', row[0])
		elif row[1]==3:
			update_sql = """update expert2017_copy set newDegree = "%s" where id = %d """%('Master', row[0])
		elif row[1]==4:
			update_sql = """update expert2017_copy set newDegree = "%s" where id = %d """%('Bachelor', row[0])
		elif row[1]==5:
			update_sql = """update expert2017_copy set newDegree = "%s" where id = %d """%('JuniorCollege', row[0])
		elif row[1]==6:
			update_sql = """update expert2017_copy set newDegree = "%s" where id = %d """%('其他', row[0])
		else:
			update_sql = """update expert2017_copy set newDegree = "%s" where id = %d """%('其他', row[0])
			
			
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
