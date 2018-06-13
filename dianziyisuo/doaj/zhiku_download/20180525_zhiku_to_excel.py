# -*- coding: utf-8 -*-

import pymysql
import pandas as pd
from pdf_file_valid import getAllFilename
def connectDatabase(my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor

def getDataByFileurlToExcel(id_list):
	db, cursor = connectDatabase()
	data_list = []
	for id in id_list:
		sql = 'select id, title, title_alternative, abstract, keywords, keywords_alternative, file_url from zhiku_data where id=%s' % id
		try:
			cursor.execute(sql)
			results = cursor.fetchone()
			# print(results)
			temp = list(results)
			temp[6] = temp[6].split('/')[2]
			data_list.append(temp)
		except Exception as e:
			print(e)
	print(len(data_list))
	data_frame = pd.DataFrame(data_list)
	data_frame.to_excel('test1.xlsx', sheet_name='sheet1', index=False,
	                    header=['id', 'title', 'title_alternative', 'abstract', 'keywords', 'keywords_alternative', 'file_url'])
	cursor.close()
	db.close()

def getDataById(id_list):
	db,cursor = connectDatabase()
	download_list = []
	for id in id_list:
		sql = 'select file_url from zhiku_data where id=%s' % id
		try:
			cursor.execute(sql)
			results = cursor.fetchone()
			print(results)
			download_list.append(results)
		except Exception as e:
			print(e)
	return download_list

def main():
	# f_zhuku_id = open('zhiku_download_list.txt', 'r')
	# id_list = f_zhuku_id.readlines()
	# for i in range(len(id_list)):
	# 	id_list[i] = id_list[i].replace('\n', '')
	# print(id_list)
	pdf_file_list = getAllFilename('./pdf_download')
	id_list = []
	for pdf in pdf_file_list:
		# print(pdf)
		id_list.append(pdf.split('.')[0])
	print(len(id_list))
	getDataByFileurlToExcel(id_list)
	# download_list = getDataById(id_list)
	# # print(download_list)
	# for d in download_list:
	# 	print(d[0])
if __name__ == '__main__':
	main()