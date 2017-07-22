# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class CbdioPipeline(object):
    def process_item(self, item, spider):
        db = pymysql.connect("127.0.0.1","root","resolution","TESTDB",charset='utf8')
        sql = "INSERT INTO testtable1(GUID,Title,DatasetID,Description,Source,Author)\
              VALUES ('%s','%s','%s','%s','%s','%s')" \
              % (item['GUID'],item['TITLE'],item['TIME'],item['DESCRIPTION'],item['SOURCE'],item['AUTHOR'])

        #print(sql)

        cursor = db.cursor()
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            print('yes')
            db.commit()
        except Exception as e:
            # 出错的话就回滚
            print(e)
            db.rollback()
        cursor.close()
        db.close()        
        return item
