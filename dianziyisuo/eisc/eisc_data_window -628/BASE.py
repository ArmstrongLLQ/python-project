# -*- coding: utf-8 -*-
'''
公有函数，处理数据库连接，excel文件数据清洗等功能
'''
import pymysql
import os
import xlrd
import xlutils.copy
import re
import datetime

# # 连接本地数据库
# def connectDatabase( my_host="localhost", my_username="root", my_keyword="", my_database="eisc_data"):
# 	# 打开数据库连接
# 	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
# 	# 使用cursor()方法获取操作游标
# 	cursor = db.cursor()
# 	return db, cursor

# 连接远程数据库
def connectDatabase( my_host="172.16.155.31", my_username="root", my_keyword="eisc15531", my_database="eisc_data"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor


# 对文件大小进行转换，小于1M的用K表示，大于1M的用M表示，保留两位小数
def fileSizeChange(filesize):
	new_filesize = int(filesize) / 1024
	if new_filesize < 1024:
		new_filesize = str(round(new_filesize)) + 'K'
	else:
		new_filesize = str(format(new_filesize / 1024, '0.2f')) + 'M'
	return new_filesize

# 读取excel文件，以列表形式返回数据
def openExcel(filename):
	try:
		data = xlrd.open_workbook(filename)
		return data
	except Exception as e:
		print(e)

#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的索引 ，by_index：表的索引
def excelTableByIndex(filename,colnameindex=0,by_index=0):
	# 获取数据
	data = openExcel(filename)
	# 获取第一个sheet的数据
	table = data.sheets()[by_index]
	nrows = table.nrows #行数
	ncols = table.ncols #列数
	colnames =  table.row_values(colnameindex) #某一行数据，默认得到表头
	table_list =[]
	for rownum in range(1,nrows):
		row = table.row_values(rownum)
		if row:
			# 把每一行的数据转换为字典的，字典的key为表头
			app = {}
			for i in range(len(colnames)):
				app[colnames[i]] = row[i]
			# 转换为字典之后将数据加入列表，最后以列表的形式返回数据
			# [{key1:value1, key2:value2,...}, {key1:value1, key2:value2,...}, ...]
			table_list.append(app)
	return table_list

# 判断excel表格里面的pdf文件是否都存在于对应的位置，test_file_filepath根据不同的文献类型不一样
# table_list:excel数据转换之后的数据列表  actual_filepath：pdf文件在磁盘的实际位置
# field_to_field_dict:字段对应关系
def fileExist(table_list, actual_filepath, field_to_field_dict):
	# count用来统计文件不存在的数量
	count = 0
	for t in table_list:
		# 获取文件名字段
		test_filename = t[field_to_field_dict['filename']]
		# 如果文件名没有pdf后缀，加上
		if '.pdf' not in test_filename:
			test_filename = test_filename + '.pdf'
		# 将actual_filepath与文件名拼接，得到绝对路径
		if test_filename[0] == '/':
			temp = actual_filepath + test_filename
		else:
			temp = actual_filepath + '/' + test_filename
		# print(temp)
		# 验证文件是否存在，不存在打印错误文件，计数器+1
		if not os.path.exists(temp):
			print(temp)
			count += 1
	if count == 0:
		print('all file exist')
		return True
	else:
		print(str(count) + ' file not exist!!!')
		return False

# 获取给定字段的index和总行数、总列数
def getIndexByTitle(excel_data, title):
	table = excel_data.sheets()[0]
	nrows = table.nrows  # 行数
	ncols = table.ncols  # 列数
	colnames = table.row_values(0)  # 第一行数据，表头

	for i in range(ncols):
		if (colnames[i] == title):
			return i, nrows, ncols
	return 0, 0, 0

# 对时间进行格式转换，转换为标准格式
# 使用正则匹配，得到年、月、日
def transTime(time):
	# 第一种 02 01 2017
	another_time = re.search(r'\d \d \d\d\d\d|\d \d\d \d\d\d\d|\d\d \d \d\d\d\d|\d\d \d\d \d\d\d\d', time)
	if another_time:
		temp = another_time.group()
		year = temp.split(' ')[2]
		if int(temp.split(' ')[0]) > 12:
			day = temp.split(' ')[0]
			month = temp.split(' ')[1]
		else:
			month = temp.split(' ')[0]
			day = temp.split(' ')[1]
		trans_time = year + '-' + month + '-' + day
		# print(trans_time)
		return trans_time

	# 2018/2/15
	another_time4 = re.search(r'\d\d\d\d/\d+/\d+', time)
	if another_time4:
		temp = another_time4.group()
		year = temp.split('/')[0]
		month = temp.split('/')[1]
		day = temp.split('/')[2]
		trans_time = year + '-' + month + '-' + day
		# print(trans_time)
		return trans_time

	# 2017/3
	another_time2 = re.search(r'\d\d\d\d/\d+', time)
	if another_time2:
		temp = another_time2.group()
		year = temp.split('/')[0]
		month = temp.split('/')[1]
		day = '1'
		trans_time = year + '-' + month + '-' + day
		# print(trans_time)
		return trans_time

	# '07 3月 2018'
	another_time3 = re.search(r'\d\d \d月 \d\d\d\d|\d\d \d\d月 \d\d\d\d', time)
	if another_time3:
		temp = another_time3.group()
		year = temp.split(' ')[2]
		month = temp.split(' ')[1].replace('月', '')
		day = temp.split(' ')[0]
		trans_time = year + '-' + month + '-' + day
		# print(trans_time)
		return trans_time

	# 20160202-20160203
	another_time5 = re.search(r'\d\d\d\d\d\d\d\d', time)
	if another_time5:
		temp = another_time5.group()
		year = temp[0:4]
		month = temp[4:6]
		day = temp[6:8]
		trans_time = year + '-' + month + '-' + day
		# print(trans_time)
		return trans_time

	# 英文日期格式
	month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
	              'November', 'December', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Sep',
	              'Oct', 'Nov', 'Dec']
	year = re.search(r'\d\d\d\d', time)
	if year:
		trans_year = year.group()
	else:
		trans_year = '2018'
	month = re.search(r'[a-zA-Z]+', time)
	if month:
		trans_month = month.group()
		trans_month = trans_month.capitalize()
		# print(trans_month)
		if trans_month == 'Sept':
			trans_month = 'Sep'
		if trans_month not in month_list:
			trans_month = '1'
			trans_day = '1'
			trans_time = trans_year + '-' + trans_month + '-' + trans_day
			return trans_time
		day = re.search(r'\d\d-|\d\d |\d-|\d |\d\d,|\d,', time)
		if day:
			trans_day = re.search(r'\d\d|\d', day.group()).group()
		else:
			trans_day = '1'
		time_temp = trans_year + ' ' + trans_month + ' ' + trans_day
		# print(time)
		try:
			time_format = datetime.datetime.strptime(time_temp, '%Y %b %d')
		except:
			time_format = datetime.datetime.strptime(time_temp, '%Y %B %d')
		trans_time = str(time_format.year) + '-' + str(time_format.month) + '-' + str(time_format.day)
		return trans_time
	else:
		trans_month = '1'
		trans_day = '1'
		trans_time = trans_year + '-' + trans_month + '-' + trans_day
		return trans_time

# 从s_source表中取出sourcename字段， select sourcename from s_source
def getSourcenameFromEisc_data():
	db, cursor = connectDatabase()
	sql = 'select sourcename from s_source'
	source_list = []
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			source_list.append(row[0])
	except Exception as e:
		print(e)
	cursor.close()
	db.close()
	return source_list

# 通过会议名查询会议对应的s_id
def getSidFromS_sourceByMeetingname(meeting_name):
	db, cursor = connectDatabase()
	sql = 'select s_id from s_source where sourcename="%s"' % meeting_name
	# print(sql)
	try:
		cursor.execute(sql)
		s_id = cursor.fetchone()
	except Exception as e:
		print(e)
	cursor.close()
	db.close()
	return s_id[0]

# 根据报告的类型获取doctype
def getDoctypeByReportTpye(report_type):
	report_type_list = ['会议', '期刊', '报告', '标准', '汇编', '论文', '专利', '专著', '参考', '文摘']
	doctype_list = ['C', 'J', 'R', 'S', 'G', 'D', 'P', 'M', 'K', 'W']
	doctype = doctype_list[report_type_list.index(report_type)]
	return doctype

# 获取要插入s_source表格的数据
def getS_sourceDataList(table_list, field_to_field_dict, report_type):
	s_source_data_list = []
	temp_list = []
	for t in table_list:
		temp_dict = {}
		for key, value in field_to_field_dict.items():
			# 如果value不为空，对value的值进行处理，存入字典
			if value != '':
				# 如果有sourcename字段，对字段的值进行判断
				if key == 'sourcename':
					# 字符串长度大于250，对字符串进行截取
					if len(t[value]) >= 250:
						temp_dict[key] = t[value][:250]
					# 字符串为空，将sourcename赋值为  No Title
					elif t[value] == '':
						temp_dict[key] = 'No Title (' + getDoctypeByReportTpye(report_type) + ')'
					# 否则，直接赋值
					else:
						temp_dict[key] = t[value]
				else:
					temp_dict[key] = t[value]
			# 如果value为空，判断key，如果是sourcename的话，赋值 No Title ，如果不是，赋值为None
			else:
				if key == 'sourcename':
					temp_dict[key] = 'No Title (' + getDoctypeByReportTpye(report_type) + ')'
				else:
					temp_dict[key] = None
		temp_dict['doctype'] = getDoctypeByReportTpye(report_type)
		temp_list.append(temp_dict)
	sourcename_list = []
	# 对sourcename进行去重
	for i in temp_list:
		if i['sourcename'] not in sourcename_list:
			sourcename_list.append(i['sourcename'])
			s_source_data_list.append(i)
	return s_source_data_list

# 插入s_source表格操作
def insertS_sourceData(s_source_data_list, source_list):
	db, cursor = connectDatabase()
	for i in s_source_data_list:
		if i['sourcename'] not in source_list:
			sql = """insert into s_source (`collectiontunit`, `isbn`, `issn`, `sourcename`, `pubdate`, `confaddress`, 
	`confdate`, `doctype`) values (%s, %s, %s, %s, %s, %s, %s, %s)"""
			value = ('电子一所文献中心', i['isbn'], i['issn'], i['sourcename'],i['pubdate'],
			         i['confaddress'], i['confdate'],i['doctype'])
			try:
				cursor.execute(sql, value)
				db.commit()
			except Exception as e:
				print('insertS_sourceData error:' + str(e))
				db.rollback()
	cursor.close()
	db.close()

# 更新s_source数据库，update s_source 按钮的回调函数
def updateS_source(new_excel_file, field_to_field_dict, report_type):
	# 从数据库中读取已有的sourcename
	source_list = getSourcenameFromEisc_data()
	# 从excel中读取数据
	table_list = excelTableByIndex(new_excel_file)
	# 得到要插入s_source表的数据
	s_source_data_list = getS_sourceDataList(table_list, field_to_field_dict, report_type)
	# 插入数据s_source
	insertS_sourceData(s_source_data_list, source_list)

# 对原来的excel文件中的某些字段的数据进行处理，然后生成一个标准格式的新的excel文件
# excel_file：excel文件   table_list：表格数据   field_to_field_dict：字段对应关系
# filepath_in_computer：filename字段处理时的路径参数
def updateData(excel_file, table_list, field_to_field_dict, filepath_in_computer):
	excel_data = openExcel(excel_file)
	if field_to_field_dict['filename'] != '':
		index_filename, nrows, ncols = getIndexByTitle(excel_data, title=field_to_field_dict['filename'])
	else:
		index_filename = 0
	if field_to_field_dict['filesize'] != '':
		index_filesize, nrows, ncols = getIndexByTitle(excel_data, title=field_to_field_dict['filesize'])
	else:
		index_filesize = 0
	if field_to_field_dict['pubdate'] != '':
		index_pubdate, nrows, ncols = getIndexByTitle(excel_data, title=field_to_field_dict['pubdate'])
	else:
		index_pubdate = 0
	if field_to_field_dict['confdate'] != '':
		index_confdate, nrows, ncols = getIndexByTitle(excel_data, title=field_to_field_dict['confdate'])
	else:
		index_confdate = 0
	if field_to_field_dict['year'] != '':
		index_year, nrows, ncols = getIndexByTitle(excel_data, title=field_to_field_dict['year'])
	else:
		index_year = 0

	# 复制一个跟原来excel一样的Excel文件
	book = xlrd.open_workbook(excel_file)
	wtbook = xlutils.copy.copy(book)
	wtsheet = wtbook.get_sheet(0)
	# 对需要转化的字段进行转化，然后写入新的excel文件中
	for i in range(1, nrows):
		if index_filename != 0:
			old_filename = table_list[i-1][field_to_field_dict['filename']].replace('\\', '/')
			if '.pdf' not in old_filename:
				old_filename = old_filename + '.pdf'
			if old_filename[0] != '/':
				old_filename = '/' + old_filename

			if field_to_field_dict['file_path'] != '':
				old_filepath = table_list[i-1][field_to_field_dict['file_path']].replace('\\', '/')
				if old_filepath[-1] == '/':
					old_filepath = old_filepath[:-1]

				old_filepath_list = old_filepath.split('/')
				if field_to_field_dict['filepath_level'] != '':
					second_filepath = ''
					filepath_level = int(field_to_field_dict['filepath_level'])
					old_filepath_list = old_filepath_list[len(old_filepath_list)-filepath_level:]
					for o in old_filepath_list:
						second_filepath += '/' + o
				else:
					second_filepath = ''
				new_filename = filepath_in_computer + second_filepath + old_filename
			else:
				new_filename = filepath_in_computer + old_filename
			wtsheet.write(i, index_filename, new_filename)

		if index_filesize != 0:
			new_filesize = fileSizeChange(table_list[i-1][field_to_field_dict['filesize']])
			wtsheet.write(i, index_filesize, new_filesize)
		if index_pubdate != 0:
			new_pubdate = transTime(table_list[i-1][field_to_field_dict['pubdate']])
			new_year = new_pubdate[:4]
			wtsheet.write(i, index_pubdate, new_pubdate)
		if index_confdate != 0:
			new_confdate = transTime(table_list[i-1][field_to_field_dict['confdate']])
			new_year = new_confdate[:4]
			wtsheet.write(i, index_confdate, new_confdate)
		if index_year != 0:
			if table_list[i-1][field_to_field_dict['year']] == '':
				wtsheet.write(i, index_year, new_year)
	filename = excel_file.split(".")[0] + '.new.xls'
	wtbook.save(filename)

# 根据不同的文献类型获取cid
def getCid(report_name):
	report_list = ['IEL', 'SPIE', 'AIAA', 'IQPC', 'AD', 'DE', 'PB', 'NASA', 'DMS', 'JANES', 'ELSEVIER', 'NTIS', 'INSPEC',
	               'EI', 'AERO', '电子科技文摘库', '硕博论文库', '科技成果库', '综合数据库', '预留数据库', '自建库']
	cid = str(report_list.index(report_name) + 1)
	return cid

def excelDataChange(excel_file, report_name, report_type, field_to_field_dict):
	table_list = excelTableByIndex(excel_file)
	data_list = []
	for t in table_list:
		temp_dict = {}
		for key, value in field_to_field_dict.items():
			if value != '':
				if key == 'sourcename':
					if len(t[value]) >= 250:
						temp_dict['sid'] = getSidFromS_sourceByMeetingname(t[value][:250])
					elif t[value] == '':
						sourcename = 'No Title (' + getDoctypeByReportTpye(report_type) + ')'
						temp_dict['sid'] = getSidFromS_sourceByMeetingname(sourcename)
					else:
						temp_dict['sid'] = getSidFromS_sourceByMeetingname(t[value])
				elif key == 'mtitle':
					try:
						if len(t[value]) >= 200:
							temp_dict[key] = t[value][:200]
						else:
							temp_dict[key] = t[value]
					except:
						temp_dict[key] = t[value]
				elif key == 'authors':
					if len(t[value]) >= 200:
						temp_dict[key] = t[value][:200]
					else:
						temp_dict[key] = t[value]
				elif key == 'authorunit':
					if len(t[value]) >= 500:
						temp_dict[key] = t[value][:500]
					else:
						temp_dict[key] = t[value]
				elif key == 'keyword':
					if len(t[value]) >= 200:
						temp_dict[key] = t[value][:200]
					else:
						temp_dict[key] = t[value]
				elif key == 'filename':
					temp_dict['filepath'] = t[value]
					temp_dict[key] = t[value].split('/')[-1]
				else:
					temp_dict[key] = t[value]
			else:
				if key == 'sourcename':
					sourcename = 'No Title (' + getDoctypeByReportTpye(report_type) + ')'
					temp_dict['sid'] = getSidFromS_sourceByMeetingname(sourcename)
				else:
					temp_dict[key] = None
		temp_dict['cid'] = getCid(report_name)
		temp_dict['encryptlevel'] = '1'
		temp_dict['language'] = 'eng'
		temp_dict['docmedia'] = 'P'

		data_list.append(temp_dict)
	return data_list

def insertNewDataToS_data(data_list, report_name):
	db, cursor = connectDatabase()
	count = 0
	cid = getCid(report_name)
	s_data_num = 's_data_' + str(int(cid) + 1000)

	for data in data_list:
		# 18个字段
		sql = 'insert into ' + s_data_num + """ (`sid`,`cid`,`year`,`vol`,`encryptlevel`,`language`,`docmedia`,`doi`,`mtitle`,
`authors`,`authorunit`,`keyword`,`abstracts`,`pages`,`bepage`,`filename`,`filepath`,`filesize`) values 
(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
		my_value = (data['sid'],data['cid'],data['year'],data['vol'],data['encryptlevel'],data['language'],
		            data['docmedia'],data['doi'],data['mtitle'],data['authors'],data['authorunit'],data['keyword'],
		            data['abstracts'],data['pages'],data['bepage'],data['filename'],data['filepath'],data['filesize'])
		# print(sql)
		try:
			cursor.execute(sql, my_value)
			db.commit()
			count += 1
		except Exception as e:
			print(e)
			db.rollback()
	cursor.close()
	db.close()
	return count

def changeDocidById(report_name):
	db, cursor = connectDatabase()
	cid = getCid(report_name)
	count = 0
	s_data_num = 's_data_' + str(int(cid) + 1000)
	sql = 'select id from ' + s_data_num + ' where docid=0'
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for r in results:
			# print(r[0])
			id = r[0]
			docid = int('1001000' + str(id))
			sql2 = 'update ' + s_data_num + ' set docid = %d where id = %d' % (docid, id)
			# print(sql2)
			try:
				cursor.execute(sql2)
				db.commit()
				count += 1
			except Exception as e:
				print(e)
				db.rollback()
	except Exception as e:
		print(e)
	cursor.close()
	db.close()
	return count

def insertErrorData(data_list, report_name):
	db, cursor = connectDatabase()
	count = 0
	cid = getCid(report_name)
	s_data_num = 's_data_' + str(int(cid) + 1000)

	sql = 'select filename from ' + s_data_num
	filename_list = []
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for r in results:
			# print(r)
			filename_list.append(r[0])
		for data in data_list:
			if data['filename'] not in filename_list:
				# 18个字段
				sql = 'insert into ' + s_data_num + """ (`sid`,`cid`,`year`,`vol`,`encryptlevel`,`language`,`docmedia`,`doi`,`mtitle`,
			`authors`,`authorunit`,`keyword`,`abstracts`,`pages`,`bepage`,`filename`,`filepath`,`filesize`) values
			(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
				my_value = (data['sid'], data['cid'], data['year'], data['vol'], data['encryptlevel'], data['language'],
				            data['docmedia'], data['doi'], data['mtitle'], data['authors'], data['authorunit'], data['keyword'],
				            data['abstracts'], data['pages'], data['bepage'], data['filename'], data['filepath'],
				            data['filesize'])
				# print(sql)
				try:
					cursor.execute(sql, my_value)
					db.commit()
					count += 1
				except Exception as e:
					print(e)
					db.rollback()
	except Exception as e:
		print(e)
	print(count)
	cursor.close()
	db.close()