import uuid
import pymysql
'''
根据id生成uuid,然后存入doaj数据库
'''
def connectDatabase( my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor

def main():
	db, cursor = connectDatabase()
	sql = 'select id from zhiku_data'

	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			print(row[0])
			my_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, str(row[0]))
			update_sql = 'update zhiku_data set uuid = "%s" where id = %d' % (my_uuid, row[0])
			print(update_sql)
			try:
				cursor.execute(update_sql)
				db.commit()

			except Exception as e:
				print(e)
				db.rollback()
	except Exception as e:
		print(e)
	cursor.close()
	db.close()
	

if __name__ == '__main__':
	main()