# coding=utf-8
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "resolution", "TESTDB")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS CBDIO")

# 使用预处理语句创建表
sql = """CREATE TABLE CBDIO(
         TITLE CHAR(100) NOT NULL,
         TIME CHAR(100),
         CONTENT CHAR(100))"""


# SQL 插入语句
sql = """INSERT INTO CBDIO(TITLE,TIME,CONTENT) VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
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

# 使用预处理语句创建表
sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,
         SEX CHAR(1),
         INCOME FLOAT )"""

cursor.execute(sql)

# 关闭数据库连接
db.close()