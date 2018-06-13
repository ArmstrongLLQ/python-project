# coding=utf-8
import requests
import pymysql
#from bs4 import BeautifulSoup as bs

def connectDatabase( my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor

langeage_list = []

sql = 'select journals_title from doaj_data GROUP BY journals_title'

count = 1
db, cursor = connectDatabase()
try:
	cursor.execute(sql)
	# 获取所有记录列表
	results = cursor.fetchall()
	for row in results:
		try:
			sql2 = """select journals_language, count(journals_language) as counts from doaj_data where journals_title="""  + '"' + str(row[0]) + '"';
			print(sql2)
			cursor.execute(sql2)
			results2 = cursor.fetchall()
			for row2 in results2:
				print('--------------------------------------------------------')
				print(row2)
				langeage_list.append(row2[0])
				print('--------------------------------------------------------')
				count += 1
		except Exception as e:
			print(e)

except Exception as e:
	print(e)

with open('catalog.txt', 'w', encoding='gbk') as f1:
	f1.writelines(langeage_list)
print(count)
# 关闭数据库连接
cursor.close()
db.close() 
