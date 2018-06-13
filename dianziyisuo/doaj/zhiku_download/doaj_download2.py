import requests
import pymysql
import os
import threading
import queue

from pdf_file_valid import getAllFilename, isValidPDF

'''
根据url下载pdf文件，然后存入指定文件夹
使用多线程加快下载速度
放在本机
'''

def connectDatabase(my_host="172.16.155.11", my_username="doaj", my_keyword="Doa123!@#j", my_database="doaj"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor

# def connectDatabase( my_host="localhost", my_username="root", my_keyword="", my_database="doaj"):
# 	# 打开数据库连接
# 	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
# 	# 使用cursor()方法获取操作游标
# 	cursor = db.cursor()
# 	return db, cursor

# 多线程模块
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

# 从数据库中读取url和uuid生成filename
def getDownloadUrlAndFilename(id_list):
	download_dict = {}
	db, cursor = connectDatabase()
	for id in id_list:
		sql = 'select id, file_url from zhiku_data where id=%s' % id
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			for row in results:
				pdf_url = row[1]
				pdf_uuid = row[0]
				pdf_filename = str(pdf_uuid) + '.pdf'

				download_dict[pdf_filename] = pdf_url

		except Exception as e:
			print(e)
	cursor.close()
	db.close()
	return download_dict

def getUrlAndFilenameFromTxt(txt_file):
	download_dict = {}
	with open(txt_file, 'r') as f:
		url_filename_list = f.readlines()
		for i in url_filename_list:
			pdf_filename = i.split(',')[0]
			pdf_url = i.split(',')[1].replace('\n', '')
			download_dict[pdf_filename] = pdf_url
		f.close()
	return download_dict

# 下载文件
def downloadFileByUrl(download_url_and_filename):
	filename = './pdf_download/' + download_url_and_filename[0]
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
	# 创建pdf_download文件夹
	if not os.path.exists('pdf_download'):
		os.mkdir('pdf_download')
	# os.chdir(os.path.join(os.getcwd(), 'pdf_download'))

	f_zhuku_id = open('zhiku_download_list.txt', 'r')
	id_list = f_zhuku_id.readlines()
	for i in range(len(id_list)):
		id_list[i] = id_list[i].replace('\n', '')
	# print(id_list)
	download_dict = getDownloadUrlAndFilename(id_list)
	#
	# download_dict = getUrlAndFilenameFromTxt('./download_fail.txt')

	# print(download_dict)
	pdf_file_list = getAllFilename('./pdf_download')
	print(len(pdf_file_list))


	download_url_queue = queue.Queue()

	for i in pdf_file_list:
		del download_dict[i]

	for filename, url in download_dict.items():
		filename_url = [filename, url]
		download_url_queue.put(filename_url)

	thread_list = []
	for i in range(50):
		thread = CrawlThread(download_url_queue)
		thread.start()
		thread_list.append(thread)

	download_url_queue.join()

	for t in thread_list:
		t.join()

	print('MainThread End')

if __name__ == '__main__':
	main()
