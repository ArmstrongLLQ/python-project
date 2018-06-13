# -*- coding: utf-8 -*-

import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CollectipsPipeline(object):
    def process_item(self, item, spider):
        
        con = pymysql.connect('localhost', '', '', 'test', charset='utf8')
        cur = con.cursor()

        sql = ("INSERT INTO xici_ip(ip, port, ip_type, speed, last_check_time) VALUES (%s, %s, %s, %s, %s)")
        lis = (item['ip'], item['port'], item['ip_type'], item['speed'], item['last_check_time'])
        try:
        	cur.execute(sql, lis)
        	con.commit()
        except Exception as e:
        	print(e)
        	con.rollback()

        cur.close()
        con.close()
        return item
