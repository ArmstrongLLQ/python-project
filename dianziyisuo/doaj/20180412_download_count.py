# coding=utf-8
import requests
import pymysql

def connectDatabase( my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor

def get_url(lines, db, cursor):
	# 得到url
	url_list = []
	for line in lines:
		journals_title  = line.replace('\n', '')

		sql = 'select id, url, journals_title, term_l1, uuid，journals_language，journals_country from doaj_data where journals_title="%s"' % journals_title
		print(sql)

		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			for result in results:
				url_list.append(result)
		except Exception as e:
			print(e)
	return url_list

def save_mysql(url_list, db, cursor):
	# 存入数据库
	for url in url_list:
		# print(url[0])
		try:
			if '.pdf' in url[1]:
				insert_sql = 'insert into doaj_url(`id`, `url`, `journals_title`, `term_l1`, `uuid`, `journals_language`, `journals_country`) values (%d, "%s", "%s", "%s", "%s", "%s", "%s")' % (url[0], url[1], url[2], url[3], url[4], url[5], url[6])
				print(insert_sql)
				try:
					cursor.execute(insert_sql)
					db.commit()
				except Exception as e:
					print(e)
					db.rollback()
			else:
				pass
		except Exception as e:
			print(e)

def count_data(db, cursor):
	# 统计数量
	count = 0
	sql = 'select url from doaj_url'
	try:
		cursor.execute(sql)
		url_list = cursor.fetchall()
		for url in url_list:
			if '.pdf' in url[0]:
				count += 1
			# print(url[0])
	except Exception as e:
		print(e)
	return count

def main():
	f_old = open('test2.txt', 'r')
	lines = f_old.readlines()
	db, cursor = connectDatabase()

	url_list = get_url(lines, db, cursor)
	# print(url_list)
	save_mysql(url_list, db, cursor)
	# count = count_data(db, cursor)
	# print(count)

	cursor.close()
	db.close()

if __name__ == '__main__':
	main()





