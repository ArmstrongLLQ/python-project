import requests
import pymysql
import os
'''
根据url下载pdf文件，然后存入指定文件夹
'''


def connectDatabase( my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor

# pdf_file = requests.get('http://www.thesai.org/Downloads/Volume8No1/Paper_51-SIT_A_Lightweight_Encryption_Algorithm_for_Secure.pdf', stream=True)
# with open('test.pdf', 'wb') as f:
# 	for chunk in pdf_file.iter_content():
# 		f.write(chunk)

def main():
	if not os.path.exists('pdf_download'):
		os.mkdir('pdf_download')
	os.chdir(os.path.join(os.getcwd(), 'pdf_download'))
	db, cursor = connectDatabase()
	sql = 'select url, uuid from doaj_url'
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			pdf_url = row[0]
			pdf_uuid = row[1]
			pdf_filename = pdf_uuid + '.pdf'
			# print(pdf_url)
			try:
				pdf_file = requests.get(pdf_url, stream=True)
				with open(pdf_filename, 'wb') as f:
					for chunk in pdf_file.iter_content():
						f.write(chunk)
			except Exception as e:
				print(e)

	except Exception as e:
		print(e)

if __name__ == '__main__':
	main()
