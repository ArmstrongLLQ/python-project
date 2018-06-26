import pymysql

# 连接远程数据库
def connectDatabase( my_host="172.16.155.31", my_username="root", my_keyword="eisc15531", my_database="eisc_data"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor

def main():
	db, cursor = connectDatabase()
	total_count = 0
	for i in range(1001, 1022):
		try:
			sql = "SELECT count(id) as a from s_data_" + str(i) + " where datetemp>'2018'"
			cursor.execute(sql)
			result = cursor.fetchone()
			total_count += int(result[0])
		except Exception as e:
			print(e)
	cursor.close()
	db.close()
	print(total_count)

main()