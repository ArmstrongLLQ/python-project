# -*- coding: utf-8 -*-
import pymysql

def insertDoajDatabase(my_host, my_username, my_keyword, my_database):
        # 打开数据库连接
        db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        sql = "INSERT INTO doaj_data(`title`, `abstract` ) VALUES (%s, %s)"
        

        raw_value = ("dddd", "In this paper, we study factorizability of (mathbb{C})-valued formal series at fixed vertices, called the graph zeta functions, induced by the reduced length on the graph groupoids of given finite connected directed graphs. The construction of such functions is motivated by that of Redei zeta functions. In particular, we are interested in (i) \"non-factorizability\" of such functions, and (ii) certain factorizable functions induced by non-factorizable functions. By constructing factorizable functions from our non-factorizable functions, we study relations between graph zeta functions and well-known number-theoretic objects, the Riemann zeta function and the Euler totient function.")
        

        try:
            # 执行sql语句
            cursor.execute(sql, raw_value)
            # 提交到数据库执行
            db.commit()
            print('insert success')
        except Exception:
            # 如果发生错误则回滚
            print('insert fail')
            raise
            db.rollback()


insertDoajDatabase("172.16.155.11", "doaj", "Doa123!@#j", "doaj")
