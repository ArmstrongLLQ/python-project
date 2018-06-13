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

def main():
	db, cursor = connectDatabase()
	f_journal_list = open('journal_list.txt', 'r')
	journal_list = f_journal_list.readlines()
	# print(journal_list)
	for i in range(len(journal_list)):
		journal_list[i] = journal_list[i].replace('\n', '')
	print(journal_list)
	sql = 'select journals_title from doaj_url'
	sql_journal_list = []
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for r in results:
			sql_journal_list.append(r[0])
	except Exception as e:
		print(e)
	print(len(set(sql_journal_list)))

	error_list = []
	for i in sql_journal_list:
		if i not in journal_list:
			error_list.append(i)
	print(list(set(error_list)))
if __name__ == '__main__':
	main()