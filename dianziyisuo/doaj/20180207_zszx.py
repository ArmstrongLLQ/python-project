import pymysql
import re


def connectDatabase(my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="zszxdataprocess"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor

def processData(db, cursor):
	select_sql = "select 关键词 from zszx_scienceachievements_20180207原始数据_copy"

	try:
		cursor.execute(select_sql)
		# 获取所有记录列表
		results = cursor.fetchall()
		print(len(results))
		for row in results:
			# print(row)
			new_row = re.sub(r'\[\d+\]', '', row[0])
			# print(new_row)
			update_sql = "update zszx_scienceachievements_20180207原始数据_copy set 关键词='%s' where 关键词='%s'"%(new_row, row[0])
			# print(update_sql)
			try:
				cursor.execute(update_sql)
				db.commit()
			except Exception as e:
				print(e)
				db.rollback()
	except Exception as e:
		print(e)



def processData2(db, cursor):
	class_set = set()
	select_sql = "select 分类号 from zszx_scienceachievements_20180207原始数据_copy"

	try:
		cursor.execute(select_sql)
		# 获取所有记录列表
		results = cursor.fetchall()
		print(len(results))
		for row in results:
			# print(row)
			new_row = re.sub(r',', ';', row[0])
			# print(new_row)
			row_list = new_row.split(';')
			for i in row_list:
				if i!='':
					print(i)
					class_set.add(i)

	except Exception as e:
		print(e)

	return class_set

def insertClassSet(db, cursor, class_set):
	for i in class_set:
		sql = "insert into class values('%s')" % i
		print(sql)
		try:
			cursor.execute(sql)
			db.commit()

		except Exception as e:
			print(e)
			db.rollback()

def processData3(db, cursor):
	select_sql = "select 分类号 from zszx_scienceachievements_20180207原始数据_copy"
	try:
		cursor.execute(select_sql)
		# 获取所有记录列表
		results = cursor.fetchall()
		print(len(results))
		for row in results:
			# print(row)
			new_row = re.sub(r',', ';', row[0])
			# print(new_row)
			patten = re.compile(r'\d+')
			num = patten.findall(new_row)
			# num = re.search(r'\d+', new_row)
			# print(num)
			num_str = ''
			for n in num:
				num_str += n + ';'
			print(num_str)
			update_sql = "update zszx_scienceachievements_20180207原始数据_copy set 分类号='%s' where 分类号='%s'" % (num_str, row[0])
			try:
				cursor.execute(update_sql)
				db.commit()
			except Exception as e:
				print(e)
				db.rollback()

	except Exception as e:
		print(e)

def getClassDict(db, cursro):
	sql = "select class, sheet from class"
	class_dict = {}
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for x in results:
			# print(x[0])
			key = re.search(r'\d+', x[0])
			# print(key.group())
			class_dict[key.group()] = x[1]

	except Exception as e:
		print(e)
		db.rollback()
	return class_dict

def replaceClass(db, cursor, class_dict):
	sql = "select 分类号 from zszx_scienceachievements_20180207原始数据_copy"
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for x in results:
			# print(x[0])
			class_list = x[0].split(';')
			new_class_list = ''
			for i in class_list:
				if i != '':
					# print(class_dict[i])
					new_class_list += class_dict[i] + ';'
			# print(new_class_list)
			update_sql = "update zszx_scienceachievements_20180207原始数据_copy set 分类号='%s' where 分类号='%s'" % (new_class_list, x[0])
			print(update_sql)
			try:
				cursor.execute(update_sql)
				db.commit()
			except Exception as e:
				print(e)
				db.rollback()

	except Exception as e:
		print(e)
		db.rollback()


def deleteFenhao(db, cursor):
	sql = "select 关键词 from zszx_scienceachievements_20180207原始数据_copy"
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for x in results:
			print(x[0][:-1])

			update_sql = "update zszx_scienceachievements_20180207原始数据_copy set 关键词='%s' where 关键词='%s'" % (x[0][:-1], x[0])
			print(update_sql)
			try:
				cursor.execute(update_sql)
				db.commit()
			except Exception as e:
				print(e)
				db.rollback()

	except Exception as e:
		print(e)
		db.rollback()
if __name__ == '__main__':


	db, cursor = connectDatabase()
	#
	# processData(db, cursor)
	# class_set = processData2(db, cursor)
	#
	# print(class_set)
	# print(len(class_set))
	#
	# insertClassSet(db, cursor, class_set)
	# processData3(db, cursor)

	# class_dict = getClassDict(db, cursor)
	# print(class_dict.values())
	# replaceClass(db, cursor, class_dict)
	deleteFenhao(db, cursor)
	cursor.close()
	db.close()

