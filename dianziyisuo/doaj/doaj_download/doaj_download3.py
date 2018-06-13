import requests
import pymysql
import os
import threading
import queue
# import logging
'''
根据url下载pdf文件，然后存入指定文件夹
使用多线程加快下载速度
放在服务器上面
'''


# def connectDatabase( my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
# 	# 打开数据库连接
# 	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
# 	# 使用cursor()方法获取操作游标
# 	cursor = db.cursor()
# 	return db, cursor

def connectDatabase( my_host="localhost", my_username="root", my_keyword="", my_database="doaj"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor
# pdf_file = requests.get('http://www.thesai.org/Downloads/Volume8No1/Paper_51-SIT_A_Lightweight_Encryption_Algorithm_for_Secure.pdf', stream=True)
# with open('test.pdf', 'wb') as f:
# 	for chunk in pdf_file.iter_content():
# 		f.write(chunk)

class CrawlThread(threading.Thread):
	def __init__(self, download_url_queue):
		threading.Thread.__init__(self)
		self.download_url_queue = download_url_queue

	def run(self):
		while True:
			print('thread start----------------------------------')
			if self.download_url_queue.empty():
				print('thread end-------------------------------------')
				break
			download_url_and_filename = self.download_url_queue.get()
			downloadFileByUrl(download_url_and_filename)
			print('thread end-------------------------------------')
			self.download_url_queue.task_done()

def getDownloadUrlAndFilename():
	download_dict = {}
	db, cursor = connectDatabase()
	sql = 'select url, uuid from doaj_url'
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			pdf_url = row[0]
			pdf_uuid = row[1]
			pdf_filename = pdf_uuid + '.pdf'

			download_dict[pdf_filename] = pdf_url

	except Exception as e:
		print(e)

	return download_dict

def downloadFileByUrl(download_url_and_filename):
	filename = download_url_and_filename[0]
	url = download_url_and_filename[1]

	# for url in download_url_and_filename.iteritems():
	# 	print(url)
	# filename = download_url_and_filename.values()
	#
	# print(url, filename)

	try:
		file_content = requests.get(url, stream=True)
		with open(filename, 'wb') as f:
			for chunk in file_content.iter_content():
				f.write(chunk)
		f.close()
	except Exception as e:
		print(e)
		with open('log.txt', 'a+') as log_file:
			log_file.write(str(filename) + '    ' + str(url) + '\n')
		log_file.close()

def main():
	if not os.path.exists('pdf_download'):
		os.mkdir('pdf_download')
	os.chdir(os.path.join(os.getcwd(), 'pdf_download'))

	# logger = logging.getLogger(__name__)
	# logger.setLevel(level=logging.INFO)
	# handler = logging.FileHandler('log.txt')
	# handler.setLevel(logging.INFO)
	# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	# handler.setFormatter(formatter)
	# logger.addHandler(handler)

	download_dict = getDownloadUrlAndFilename()

	# print(download_dict)

	download_url_queue = queue.Queue()
	# download_url_queue.put(download_dict)

	for key, value in download_dict.items():
		# temp_dict.clear()
		# temp_list.clear()
		# temp_list.append(key)
		# temp_list.append(value)
		key_value = [key, value]
		download_url_queue.put(key_value)

	for i in range(10):
		thread = CrawlThread(download_url_queue)
		thread.start()

	download_url_queue.join()

	for i in range(10):
		thread.join()

	print('MainThread End')

if __name__ == '__main__':
	main()
