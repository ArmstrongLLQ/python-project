# -*- coding: utf-8 -*-
import pymysql
from pdf_file_valid import getAllFilename
import os

def connectDatabase(my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor

def langyujie():
	db, cursor = connectDatabase()
	f = open('1.txt', 'r', encoding='utf-8')
	organ_list = f.readlines()
	for i in range(len(organ_list)):
		organ_list[i] = organ_list[i].replace('\n', '')
	# print(organ_list)
	sql = 'SELECT DISTINCT(reference) FROM zhiku_data'
	reference_list = []
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		# print(results)
		for r in results:
			reference_list.append(r[0])
	except Exception as e:
		print(e)
	# print(reference_list)
	for o in organ_list:
		for r in reference_list:
			if o == r:
				print(r)
	cursor.close()
	db.close()

def rename():
	db, cursor = connectDatabase()
	sql = 'SELECT id, uuid FROM zhiku_data'
	id_uuid_dict = {}
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for r in results:
			id_uuid_dict[str(r[0])] = r[1]
	except Exception as e:
		print(e)
	file_list = getAllFilename('./pdf_download')

	# print(file_list)

	for f in file_list:
		key = f.split('.')[0]
		new_filename = id_uuid_dict[key] + '.pdf'
		print(new_filename)
		os.rename('./pdf_download/'+f, './pdf_download/'+new_filename)
	#
	# new_file_list = []
	cursor.close()
	db.close()

def main():
	rename()
if __name__ == '__main__':
	main()
