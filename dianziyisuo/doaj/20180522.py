# coding=utf-8
'''
向doaj_url里面插入新的字段journals_language, journals_country
'''
import pymysql
import os
from collections import Counter

def connectDatabase( my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor

def updateDataDoaj_url():
	db, cursor = connectDatabase()
	sql = 'select id from doaj_url'
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		id_list = []
		for r in results:
			id_list.append(r[0])
	except Exception as e:
		print(e)

	for id in id_list:
		sql = 'select article_created_date from doaj_data where id="%s"' % id
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			# print(results)
			for r in results:
				sql2 = 'update doaj_url set article_created_date="%s" where id="%s"' % (r[0], id)
				try:
					cursor.execute(sql2)
					db.commit()
				except Exception as e:
					print(e)
					db.rollback()
		except Exception as e:
			print(e)
	cursor.close()
	db.close()

def getAllFilename(path):
	pdf_file_list = []
	for i in os.walk(path):
		pdf_file_list = i[-1]
	return pdf_file_list

def main():
	# updateDataDoaj_url()
	download_success_pdf_list = getAllFilename('D:/lilanqing/Project_local/python/dianziyisuo/doaj/doaj_download/pdf_download2')
	for i in range(len(download_success_pdf_list)):
		download_success_pdf_list[i] = download_success_pdf_list[i].split('.')[0]
	# print(download_success_pdf_list)
	db, cursor = connectDatabase()
	sql = 'select article_created_date, uuid from doaj_url'
	article_created_date_list = []
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for r in results:
			if r[1] in download_success_pdf_list:
				article_created_date_list.append(r[0])
	except Exception as e:
		print(e)
	# print(article_created_date_list)
	year_list = range(2006,2017)
	for year in year_list:
		article_after_2016 = []
		for a in article_created_date_list:
			if a > str(year):
				article_after_2016.append(a)
		print(len(article_after_2016))
	# article_after_2016.sort()
	# print(article_after_2016)
	# article_created_date_list.sort()
	# print(article_created_date_list)
	cursor.close()
	db.close()

if __name__ == '__main__':
	main()