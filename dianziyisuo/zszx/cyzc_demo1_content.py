# -*- coding: utf-8 -*-
import pymysql
from bs4 import BeautifulSoup

db = pymysql.connect("172.16.155.92","root","myzszx002","zszx2017",charset = "utf8", port=3326)
cursor = db.cursor()


sql = "select id,content from cyzc2017_copy"

try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		soup = BeautifulSoup(row[1], 'lxml')
		new_content = ""
		if soup.find('div'):
			for para in soup.find_all('div'):
				new_content += para.get_text()
				new_content = new_content.replace("'", "\\'")
				new_content = new_content.replace('"', '\\"')
		elif soup.find('p'):
			for para in soup.find_all('p'):
				new_content += para.get_text()
			if  new_content == "":
				for para in soup.find_all('table'):
					new_content += para.get_text()
				new_content = new_content.replace("'", "\\'")
				new_content = new_content.replace('"', '\\"')
		else:
			for para in soup.find_all('table'):
				new_content += para.get_text()
			if new_content == "":
				for para in soup.find_all('p'):
					new_content += para.get_text()
				new_content = new_content.replace("'", "\\'")
				new_content = new_content.replace('"', '\\"')

		update_sql = """update cyzc2017_copy set newContent = \'%s\' where id = %d """%(new_content, row[0])
		try:
			cursor.execute(update_sql)
			db.commit()
		except:
			print(new_content)
			print("error1")
			print(update_sql)
			print(row[0])
			raise 
			print('\n')

except:
	print("error2")
	raise
	db.rollback()
cursor.close()
db.close()
