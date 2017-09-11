 # -*- coding: utf-8 -*- 
import pymysql
from bs4 import BeautifulSoup

db = pymysql.connect("172.16.155.12","root","myzszx002","zszx2017",charset = "utf8")
cursor = db.cursor()


sql = "select Achievement from expert2017_copy"

try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		soup = BeautifulSoup(row[0], 'lxml')
		new_achievement = ""
		for para in soup.find_all('p'):
			new_achievement += para.get_text()
		new_achievement = new_achievement.replace("'", "\\'")
		new_achievement = new_achievement.replace('"', '\\"')
		string1 = row[0]
		string1 = string1.replace("'", "\\'")
		string1 = string1.replace('"', '\\"')
		update_sql = """update expert2017_copy set newAchievement = "%s" where Achievement = "%s" """%(new_achievement, string1)
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

sql = "select Achievement from expert2017_copy"

try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		soup = BeautifulSoup(row[0], 'lxml')
		new_achievement = ""
		for para in soup.find_all('div'):
			new_achievement += para.get_text()
		if(new_achievement != ""):
			update_sql = """update expert2017_copy set newAchievement = "%s" where Achievement = "%s" """%(new_achievement, row[0])
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

# soup = BeautifulSoup(html_doc, 'lxml')
# for para in soup.find_all('p'):
# 	print(para.get_text())


# html_doc = """
# <p><span style="font: 14px/24px arial, 宋体, sans-serif; color: rgb(51, 51, 51); text-transform: none; text-indent: 28px; letter-spacing: normal; word-spacing: 0px; float: none; display: inline !important; white-space: normal; widows: 1; font-size-adjust: none; font-stretch: normal; background-color: rgb(255, 255, 255); -webkit-text-stroke-width: 0px;">李同保长期从事光辐射计量测试技术研究，是国际上最早从事量子辐射学研究的科学家之一，主持研制的多项光辐射测量标准及仪器填补了国内空白。在60年代，研制了2000K -- 2854K色温临时工作标准，满足了光度、色度，以及光探测器积分灵敏度标定方面的急需。他研制的微弱光标准测试装置，提出一种测量极低透过率（nx l0-6）的新方法，使得能以5%的不确定度测量l0-6Lx水平的微光照度，满足了当时夜视微光器件、放射萤光材料等国防科研生产的急需。在70年代，研制了我国第一台精密数字式照度计，该仪器在V（λ）函数修正、余弦特性校准、直线性校准，准确度及长期稳定性等方面都达到当时国际上同类仪器的水平。在建立500K --- 1000K全辐照标准工作中，改进了辐射腔测温结构和测量程序，显著地提高了黑体辐射器的品质，为我国红外制导和红外武器系统的科研生产提供了检测的技术基础。1977年，他主持完成最大光谱光效率（Km值）实验测定，测定值非常接近同期9个国家标准实验室测出Km值的平均值。工作受到国际计量局和国际光度与辐射度咨询委员会的重视和赞扬。在80年代初，他利用Kr+ 和Ar+ 激光器、倍频技术和自校准硅光电二极管，以0．5%一1%的不确定度测量了硅在紫外区的量于产额，比国际通常采用的克里斯坦森数据其精度提高约5倍。在以后的“用硅光二极管自校准技术实现400 --- 900nm光谱辐射绝对测量”的研究中，对零偏压下动态电阻进行了深入的研究，结合外部特征参数的精密测试，对器件的预选择提出了有效判据。在当时是处于国际领先地位。李同保主持和参与的科研项目，曾2次获国家科技进步壹等奖，多次获省部级科技奖励。他的30多篇研究论文受到国际光辐射计量界的重视并有较大的影响。</span></p>
# """


