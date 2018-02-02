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

terms = ['Mathematics', 'mathematics','computers', 'Computers', 'information','Information' ,'communication','communication', 'Chemistry','chemistry', 'circuit','Circuit','Electrical', 'electrical']
math_count = 0
computer_count = 0
information_count = 0
communication_count = 0
chemistry_count = 0
circuit_count = 0
electrical_count = 0

term_list = []
f_old = open('test2.txt', 'r')
lines = f_old.readlines()
# print(lines)
db, cursor = connectDatabase()
for line in lines:
	temp = line.replace('\n','')

	# 统计数量
	# sql = 'select count(*) from doaj_data where year<=2015 and journals_title=' + "'" + temp + "'"

	sql = 'select term from doaj_data where year<=2015 and journals_title=' + "'" + temp + "'"
	try:
		cursor.execute(sql)
		results = cursor.fetchone()
		print(results)
		# if terms[0] in results or terms[1] in results:
		# 	math_count += 1
		# if terms[2] in results or terms[3] in results:
		# 	computer_count += 1
		# if terms[4] in results or terms[5] in results:
		# 	information_count += 1
		# if terms[6] in results or terms[7] in results:
		# 	communication_count += 1
		# if terms[8] in results or terms[9] in results:
		# 	chemistry_count += 1
		# if terms[10] in results or terms[11] in results:
		# 	circuit_count += 1
		# if terms[12] in results or terms[13] in results:
		# 	electrical_count += 1
		term_list.append(results)
		# print('--------------------------------')
	except Exception as e:
		print(e)
cursor.close()
db.close()

print(term_list)
# print(math_count, computer_count, information_count, communication_count, chemistry_count, circuit_count, electrical_count)
#
# langeage_list = []
#
# sql = 'select journals_title from doaj_data GROUP BY journals_title'
#
# count = 1


# try:
# 	cursor.execute(sql)
# 	# 获取所有记录列表
# 	results = cursor.fetchall()
# 	for row in results:
# 		try:
# 			sql2 = """select journals_language, count(journals_language) as counts from doaj_data where journals_title="""  + '"' + str(row[0]) + '"';
# 			print(sql2)
# 			cursor.execute(sql2)
# 			results2 = cursor.fetchall()
# 			for row2 in results2:
# 				print('--------------------------------------------------------')
# 				print(row2)
# 				langeage_list.append(row2[0])
# 				print('--------------------------------------------------------')
# 				count += 1
# 		except Exception as e:
# 			print(e)
#
# except Exception as e:
# 	print(e)
#
# print(count)
# # 关闭数据库连接
# cursor.close()
# db.close()


