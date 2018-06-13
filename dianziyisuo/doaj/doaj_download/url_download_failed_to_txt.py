# -*- coding: utf-8 -*-
'''
将下载失败的pdf文件的url和txt文件
'''

import os
import pymysql

def connectDatabase( my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor

# 从数据库中读取url和uuid生成filename
def getDownloadUrlAndFilename():
	download_dict = {}
	db, cursor = connectDatabase()
	sql = 'select url, uuid from doaj_url'
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			pdf_url = row[0]
			pdf_uuid = row[1]
			pdf_filename = pdf_uuid + '.pdf'

			download_dict[pdf_filename] = pdf_url

	except Exception as e:
		print(e)

	return download_dict

def getAllFilename(path):
	pdf_file_list = []
	for i in os.walk(path):
		pdf_file_list = i[2]
	return pdf_file_list

def getUUID(pdf_file_list):
	uuid_list = []
	for pdf in pdf_file_list:
		uuid = pdf.split('.')[0]
		uuid_list.append(uuid)
	return uuid_list

def main():
	pdf_file_list = getAllFilename('./pdf_download')
	# print(pdf_file_list)
	# uuid_list = getUUID(pdf_file_list)
	# print(uuid_list)

	download_dict = getDownloadUrlAndFilename()

	download_fail_dict = {}
	for k, v in download_dict.items():
		if k not in pdf_file_list:
			download_fail_dict[k] = v


	print(len(download_fail_dict))
	with open('download_fail.txt', 'a+') as f:
		for k, v in download_fail_dict.items():
			f.writelines(k+','+v+'\n')

	f.close()


if __name__ == '__main__':
	main()