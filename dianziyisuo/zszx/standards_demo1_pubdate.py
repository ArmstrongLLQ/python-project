# -*- coding: utf-8 -*-
# 使用正则表达式匹配不符合要求的时间格式，将其替换成标准格式时间
import pymysql
from bs4 import BeautifulSoup
import re

def match_str(str):
	sub_str = ""
	# 匹配XXXX-/.XX-/.XX
	if re.match(r'\d{4}(\-|\/|\.)\d{1,2}(\-|\.)\d{1,2}', str):
		sub_str = re.sub(r'\D','-',str)
	# 匹配XXXX年XX月XX日
	elif re.match(r'\d{4}年\d{1,2}月\d{1,2}日', str):
		sub_str = re.sub(r'日', '', re.sub(r'年|月', '-', str))
	# 匹配只有年的
	elif re.fullmatch(r'\d{4}',str):
		sub_str = re.fullmatch(r'\d{4}',str).group() + '-01-01'
	# 匹配英文格式日期
	elif re.match(r'\d{1,2}.[A-Z,a-z,.]*.\d{4}', str):
		result = re.match(r'\d{1,2}.[A-Z,a-z,.]*.\d{4}', str)
		day = re.match(r'\d{1,2}', str).group()
		year = re.search(r'\d{4}', str).group()
		print(day,year)
		if re.search(r'Jan', result.group()):
			month = '01'
		elif re.search(r'Feb', result.group()):
			month = '02'
		elif re.search(r'Mar', result.group()):
			month = '03'
		elif re.search(r'Apr', result.group()):
			month = '04'
		elif re.search(r'May', result.group()):
			month = '05'
		elif re.search(r'Jun', result.group()):
			month = '06'
		elif re.search(r'Jul', result.group()):
			month = '07'
		elif re.search(r'Aug', result.group()):
			month = '08'
		elif re.search(r'Sep', result.group()):
			month = '09'
		elif re.search(r'Oct', result.group()):
			month = '10'
		elif re.search(r'Nov', result.group()):
			month = '11'
		elif re.search(r'Dec', result.group()):
			month = '12'
		else:
			sub_str = ""
		sub_str = year + '-' + month + '-' + day
	return sub_str

db = pymysql.connect("172.16.155.12","root","myzszx002","zszxalldata",charset = "utf8")
cursor = db.cursor()


sql = "select id,PubDate,newPubDate,ImpleDate,newImpleDate,StopDate,newStopDate from zszx_standards_copy"

try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		if row[2] == None:
			new_pub_date = match_str(row[1])
			new_imple_date = match_str(row[3])
			new_stop_date = match_str(row[5])

			# 同时更新三个时间字段
			update_sql = """update zszx_standards_copy set newPubDate = '%s',newImpleDate = '%s',newStopDate = '%s' 
							where id = %d """%(new_pub_date, new_imple_date, new_stop_date, row[0])
			try:
				cursor.execute(update_sql)
				db.commit()
			except:
				print("error1")
				print(row[0])
				raise
				print('\n')

except:
	print("error2")
	raise
	db.rollback()
cursor.close()
db.close()
