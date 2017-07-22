# coding=utf-8
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost","root","resolution","TESTDB" )

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 插入语句
sql = """INSERT INTO CBDIO7(TITLE,TIME,CONTENT) VALUES ('央企聚力国家大数据(贵州)综合试验区建设','2016-12-22 09:25', '2016年岁末,国务院国资委率阵容强大的中央企业来到贵阳,为蓬勃发展的贵州大数据产业注入强劲的央企力量。 详细')"""
print(sql)
try:
   # 执行sql语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
except:
   # 如果发生错误则回滚
   db.rollback()

# 关闭数据库连接
db.close()
