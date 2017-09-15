# -*- coding: utf-8 -*-
import pymysql
from bs4 import BeautifulSoup

db = pymysql.connect("172.16.155.12","root","myzszx002","zszx2017",charset = "utf8")
cursor = db.cursor()


sql = "select id,Achievement from expert2017_copy"

try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		soup = BeautifulSoup(row[1], 'lxml')
		new_achievement = ""
		for para in soup.find_all('p'):
			new_achievement += para.get_text()
		new_achievement = new_achievement.replace("'", "\\'")
		new_achievement = new_achievement.replace('"', '\\"')

		update_sql = """update expert2017_copy set newAchievement = "%s" where id = %d"""%(new_achievement, row[0])
		try:
			cursor.execute(update_sql)
			db.commit()
		except:
			print("error",)
			db.rollback()
		print('\n')

except:
	print("error")
	db.rollback()

sql = "select id,Achievement from expert2017_copy"

try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		soup = BeautifulSoup(row[1], 'lxml')
		new_achievement = ""
		for para in soup.find_all('div'):
			new_achievement += para.get_text()
		new_achievement = new_achievement.replace("'", "\\'")
		new_achievement = new_achievement.replace('"', '\\"')
		if(new_achievement != ""):
			update_sql = """update expert2017_copy set newAchievement = "%s" where id = %d"""%(new_achievement, row[0])
			print(update_sql)
			try:
				cursor.execute(update_sql)
				db.commit()
			except:
				print("error",)
				db.rollback()
			print('\n')

except:
	print("error")
	db.rollback()
cursor.close()
db.close()



