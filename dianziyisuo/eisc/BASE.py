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


# 对文件大小进行转换，小于1M的用K表示
def fileSizeChange(filesize):
	new_filesize = int(filesize) / 1024
	if new_filesize < 1024:
		new_filesize = str(round(new_filesize)) + 'K'
	else:
		new_filesize = str(format(new_filesize / 1024, '0.2f')) + 'M'
	return new_filesize

def openExcel(filename):
	try:
		data = xlrd.open_workbook(filename)
		return data
	except Exception as e:
		print(e)

#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excelTableByIndex(filename,colnameindex=0,by_index=0):
	data = openExcel(filename)
	table = data.sheets()[by_index]
	nrows = table.nrows #行数
	ncols = table.ncols #列数
	colnames =  table.row_values(colnameindex) #某一行数据
	table_list =[]
	for rownum in range(1,nrows):
		row = table.row_values(rownum)
		if row:
			app = {}
			for i in range(len(colnames)):
				app[colnames[i]] = row[i]
			table_list.append(app)
	return table_list

# 判断excel表格里面的pdf文件是否都存在于对应的位置，test_file_filepath根据不同的文献类型不一样
def fileExist(table_list, actual_filepath):
	count = 0
	for t in table_list:
		t_keys = t.keys()
		if 'filename' in t_keys:
			test_filename = t['filename'].replace('\\', '/')
		else:
			test_filename = t['FileName'].replace('\\', '/')

		if test_filename[0] == '/':
			temp = actual_filepath + test_filename
		else:
			temp = actual_filepath + '/' + test_filename
		# print(temp)
		if not os.path.exists(temp):
			print(temp)
			count += 1
	if count == 0:
		print('all file exist')
		return True
	else:
		print(str(count) + ' file not exist!!!')
		return False

# 获取filename字段的index
def getIndexByTitle(excel_file, title):
	data = openExcel(excel_file)
	table = data.sheets()[0]
	nrows = table.nrows  # 行数
	ncols = table.ncols  # 列数
	colnames = table.row_values(0)  # 第一行数据

	for i in range(ncols):
		if (colnames[i] == title):
			return i, nrows, ncols
	return 0, 0, 0

def transTime(time):
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

	another_time2 = re.search(r'\d\d\d\d/\d\d', time)
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

# 从s_source表中取出sourcename字段
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

# 从excel表格中将meeting的数据取出来，然后去重，得到meeting_list，下一步将meeting_list的内容存入s_source中
def getMeetinglist(table_list):
	meeting_list_temp = []
	i_keys = table_list[0].keys()
	for i in table_list:
		meeting_dict = {}
		if 'MeetingName' in i_keys:
			if len(i['MeetingName']) >= 250:
				meeting_dict['Meetingname'] = i['MeetingName'][:250]
			else:
				meeting_dict['Meetingname'] = i['MeetingName']
		else:
			if len(i['Meetingname']) >= 250:
				meeting_dict['Meetingname'] = i['Meetingname'][:250]
			else:
				meeting_dict['Meetingname'] = i['Meetingname']
		if 'MeetingDate' in i_keys:
			meeting_dict['MeetingDate'] = transTime(i['MeetingDate'])
		else:
			meeting_dict['MeetingDate'] = transTime(i['Meetingdate'])
		meeting_dict['MeetingAddress'] = i['MeetingAddress']
		if 'isbn' in i_keys:
			meeting_dict['ISBN'] = i['isbn']
		else:
			meeting_dict['ISBN'] = i['ISBN']
		if 'publicationDate' in i_keys:
			meeting_dict['publicationDate'] = transTime(i['publicationDate'])
		elif 'publicationdate' in i_keys:
			meeting_dict['publicationDate'] = transTime(i['publicationdate'])
		else:
			meeting_dict['publicationDate'] = None
		meeting_list_temp.append(meeting_dict)
	meeting_list = []
	meetingname_list = []
	for m in meeting_list_temp:
		if m['Meetingname'] not in meetingname_list:
			meetingname_list.append(m['Meetingname'])
			meeting_list.append(m)
	return meeting_list

def getJournalList(table_list):
	journal_list_temp = []
	i_keys = table_list[0].keys()
	for i in table_list:
		journal_dict = {}
		if 'journalname' in i_keys:
			journal_dict['journalname'] = i['journalname']
		else:
			journal_dict['journalname'] = i['JournalName']
		if 'issn' in i_keys:
			journal_dict['issn'] = i['issn']
		else:
			journal_dict['issn'] = i['ISSN']
		journal_list_temp.append(journal_dict)
	journal_list = []
	journalname_list = []
	for j in journal_list_temp:
		if j['journalname'] not in journalname_list:
			journalname_list.append(j['journalname'])
			journal_list.append(j)
	return journal_list

def getReportList(table_list):
	report_list_temp = []
	i_keys = table_list[0].keys()
	for i in table_list:
		report_dict = {}
		if 'Technical Report' in i['TitleNote']:
			report_dict['sourcename'] = 'Technical Report'
		else:
			report_dict['sourcename'] = i['TitleNote']
		report_list_temp.append(report_dict)
	report_list = []
	sourcename_list = []
	for r in report_list_temp:
		if r['sourcename'] not in sourcename_list:
			sourcename_list.append(r['sourcename'])
			report_list.append(r)
	return report_list

def getHuibianList(table_list):
	huibian_list_temp = []
	i_keys = table_list[0].keys()
	for i in table_list:
		huibian_dict = {}
		if 'Publication' in i_keys:
			huibian_dict['sourcename'] = i['Publication']
		else:
			huibian_dict['sourcename'] = i['publication']
		huibian_list_temp.append(huibian_dict)
	huibian_list = []
	sourcename_list = []
	for r in huibian_list_temp:
		if r['sourcename'] not in sourcename_list:
			sourcename_list.append(r['sourcename'])
			huibian_list.append(r)
	return huibian_list

# 将s_source表里面原来不存在的meeting插入
def insertS_sourceByMeeting(meeting_list, source_list):
	db, cursor = connectDatabase()
	for m in meeting_list:
		if m['Meetingname'] not in source_list:
			try:
				sql = 'insert into s_source (`collectiontunit`,`isbn`,`sourcename`,`pubdate`,`confaddress`,`confdate`,`doctype`) \
	VALUES ("%s","%s","%s","%s","%s","%s","%s")' % \
				      ('电子一所文献中心', m['ISBN'], m['Meetingname'], m['publicationDate'], m['MeetingAddress'],
				       m['MeetingDate'], 'C')
				# print(sql)
				cursor.execute(sql)
				db.commit()
			except Exception as e:
				print(e)
				db.rollback()
	cursor.close()
	db.close()

# 将s_source表里面原来不存在的journal插入
def insertS_sourceByJournal(journal_list, source_list):
	db, cursor = connectDatabase()
	for j in journal_list:
		if j['journalname'] not in source_list:
			try:
				sql = 'insert into s_source (`collectiontunit`,`issn`,`sourcename`,`doctype`) VALUES ("%s","%s","%s","%s")' % \
				      ('电子一所文献中心', j['issn'], j['journalname'], 'J')
				# print(sql)
				cursor.execute(sql)
				db.commit()
			except Exception as e:
				print(e)
				db.rollback()
	cursor.close()
	db.close()

def insertS_sourceByReport(report_list, source_list):
	db, cursor = connectDatabase()
	for r in report_list:
		if r['sourcename'] not in source_list:
			try:
				sql = 'insert into s_source (`collectiontunit`,`sourcename`,`doctype`) VALUES ("%s","%s","%s")' % \
				      ('电子一所文献中心', r['sourcename'], 'R')
				# print(sql)
				cursor.execute(sql)
				db.commit()
			except Exception as e:
				print(e)
				db.rollback()
	cursor.close()
	db.close()

def insertS_sourceByHuibian(huibian_list, source_list):
	db, cursor = connectDatabase()
	for r in huibian_list:
		if r['sourcename'] not in source_list:
			try:
				sql = 'insert into s_source (`collectiontunit`,`sourcename`,`doctype`) VALUES ("%s","%s","%s")' % \
				      ('电子一所文献中心', r['sourcename'], 'G')
				# print(sql)
				cursor.execute(sql)
				db.commit()
			except Exception as e:
				print(e)
				db.rollback()
	cursor.close()
	db.close()

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

def finalMeeting(excel_filename):
	source_list = getSourcenameFromEisc_data()
	table_list = excelTableByIndex(excel_filename)
	meeting_list = getMeetinglist(table_list)
	insertS_sourceByMeeting(meeting_list, source_list)

def finalJournal(excel_filename):
	source_list = getSourcenameFromEisc_data()
	table_list = excelTableByIndex(excel_filename)
	journal_list = getJournalList(table_list)
	insertS_sourceByJournal(journal_list, source_list)

def finalReport(excel_filename):
	source_list = getSourcenameFromEisc_data()
	table_list = excelTableByIndex(excel_filename)
	report_list = getReportList(table_list)
	insertS_sourceByReport(report_list, source_list)

def finalHuibian(excel_filename):
	source_list = getSourcenameFromEisc_data()
	table_list = excelTableByIndex(excel_filename)
	huibian_list = getHuibianList(table_list)
	insertS_sourceByHuibian(huibian_list, source_list)

def updateData(excel_file, table_list, report_type, filepath_in_computer):
	# 得到excel里面的字段，存入t_keys列表
	t_keys = table_list[0].keys()
	if report_type == 'QK':
		if 'filename' in t_keys:
			index_filename, nrows, ncols = getIndexByTitle(excel_file, title='filename')
		else:
			index_filename, nrows, ncols = getIndexByTitle(excel_file, title='FileName')

		if 'filesize' in t_keys:
			index_filesize, nrows, ncols = getIndexByTitle(excel_file, title='filesize')
		else:
			index_filesize, nrows, ncols = getIndexByTitle(excel_file, title='FileSize')

		if 'issueDate' in t_keys:
			index_issue_date, nrows, ncols = getIndexByTitle(excel_file, title='issueDate')
		elif 'issuedate' in t_keys:
			index_issue_date, nrows, ncols = getIndexByTitle(excel_file, title='issuedate')
		else:
			index_issue_date = 0

		index_year, nrows, ncols = getIndexByTitle(excel_file, title='year')

		if(index_filename == 0 or index_filesize == 0):
			print(excel_file)
		else:
			book = xlrd.open_workbook(excel_file)
			wtbook = xlutils.copy.copy(book)
			wtsheet = wtbook.get_sheet(0)
			for i in range(1, nrows):
				if 'filename' in t_keys:
					old_filepath = table_list[i-1]['filename'].replace('\\', '/')
				else:
					old_filepath = table_list[i-1]['FileName'].replace('\\', '/')

				if old_filepath[0] == '/':
					new_filepath = filepath_in_computer + old_filepath
				else:
					new_filepath = filepath_in_computer + '/' + old_filepath

				if 'filesize' in t_keys:
					new_filesize = fileSizeChange(table_list[i-1]['filesize'])
				else:
					new_filesize = fileSizeChange(table_list[i-1]['FileSize'])

				if 'issueDate' in t_keys:
					new_issue_date = transTime(table_list[i-1]['issueDate'])
				elif 'issuedate' in t_keys:
					new_issue_date = transTime(table_list[i - 1]['issuedate'])
				else:
					new_issue_date = None

				if table_list[i-1]['year'] == '':
					if new_issue_date != None:
						new_year = new_issue_date[:4]
						wtsheet.write(i, index_year, new_year)
				# print(new_filepath)
				wtsheet.write(i, index_filename, new_filepath)
				wtsheet.write(i, index_filesize, new_filesize)
				if index_issue_date != 0:
					wtsheet.write(i, index_issue_date, new_issue_date)
			filename = excel_file.split(".")[0] + '.new.xls'
			print('success generate: ' + filename)
			wtbook.save(filename)
	elif report_type == 'HY':
		if 'filename' in t_keys:
			index_filename, nrows, ncols = getIndexByTitle(excel_file, title='filename')
		else:
			index_filename, nrows, ncols = getIndexByTitle(excel_file, title='FileName')

		if 'filesize' in t_keys:
			index_filesize, nrows, ncols = getIndexByTitle(excel_file, title='filesize')
		else:
			index_filesize, nrows, ncols = getIndexByTitle(excel_file, title='FileSize')

		if 'MeetingDate' in t_keys:
			index_meeting_date, nrows, ncols = getIndexByTitle(excel_file, title='MeetingDate')
		else:
			index_meeting_date, nrows, ncols = getIndexByTitle(excel_file, title='Meetingdate')

		if 'publicationDate' in t_keys:
			index_publication_date, nrows, ncols = getIndexByTitle(excel_file, title='publicationDate')
		else:
			index_publication_date = 0

		index_year, nrows, ncols = getIndexByTitle(excel_file, title='year')

		if (index_filename == 0 or index_filesize == 0):
			print(excel_file)
		else:
			book = xlrd.open_workbook(excel_file)
			wtbook = xlutils.copy.copy(book)
			wtsheet = wtbook.get_sheet(0)
			for i in range(1, nrows):
				if 'filename' in t_keys:
					old_filepath = table_list[i-1]['filename'].replace('\\', '/')
				else:
					old_filepath = table_list[i-1]['FileName'].replace('\\', '/')

				if old_filepath[0] == '/':
					new_filepath = filepath_in_computer + old_filepath
				else:
					new_filepath = filepath_in_computer + '/' + old_filepath

				if 'filesize' in t_keys:
					new_filesize = fileSizeChange(table_list[i-1]['filesize'])
				else:
					new_filesize = fileSizeChange(table_list[i-1]['FileSize'])

				if 'MeetingDate' in t_keys:
					new_meeting_date = transTime(table_list[i - 1]['MeetingDate'])
				else:
					new_meeting_date = transTime(table_list[i - 1]['Meetingdate'])

				if 'publicationDate' in t_keys:
					new_publication_date = transTime(table_list[i - 1]['publicationDate'])
				else:
					new_publication_date = None

				if table_list[i-1]['year'] == '':
					new_year = new_meeting_date[:4]
					wtsheet.write(i, index_year, new_year)
				# print(new_filepath)
				wtsheet.write(i, index_filename, new_filepath)
				wtsheet.write(i, index_filesize, new_filesize)
				wtsheet.write(i, index_meeting_date, new_meeting_date)
				wtsheet.write(i, index_publication_date, new_publication_date)
			filename = excel_file.split(".")[0] + '.new.xls'
			print(filename)
			wtbook.save(filename)
	elif report_type == 'report':
		if 'filename' in t_keys:
			index_filename, nrows, ncols = getIndexByTitle(excel_file, title='filename')
		else:
			index_filename, nrows, ncols = getIndexByTitle(excel_file, title='FileName')

		if 'filesize' in t_keys:
			index_filesize, nrows, ncols = getIndexByTitle(excel_file, title='filesize')
		else:
			index_filesize, nrows, ncols = getIndexByTitle(excel_file, title='FileSize')

		if 'publicationDate' in t_keys:
			index_publication_date, nrows, ncols = getIndexByTitle(excel_file, title='publicationDate')
		else:
			index_publication_date, nrows, ncols = getIndexByTitle(excel_file, title='publicationdate')

		index_year, nrows, ncols = getIndexByTitle(excel_file, title='year')

		if(index_filename == 0 or index_filesize == 0):
			print(excel_file)
		else:
			book = xlrd.open_workbook(excel_file)
			wtbook = xlutils.copy.copy(book)
			wtsheet = wtbook.get_sheet(0)
			for i in range(1, nrows):
				if 'filename' in t_keys:
					old_filepath = table_list[i-1]['filename'].replace('\\', '/')
				else:
					old_filepath = table_list[i-1]['FileName'].replace('\\', '/')

				if old_filepath[0] == '/':
					new_filepath = filepath_in_computer + old_filepath
				else:
					new_filepath = filepath_in_computer + '/' + old_filepath

				if 'filesize' in t_keys:
					new_filesize = fileSizeChange(table_list[i-1]['filesize'])
				else:
					new_filesize = fileSizeChange(table_list[i-1]['FileSize'])

				if 'publicationDate' in t_keys:
					new_publication_date = transTime(table_list[i-1]['publicationDate'])
				else:
					new_publication_date = transTime(table_list[i - 1]['publicationdate'])

				if table_list[i-1]['year'] == '':
					new_year = new_publication_date[:4]
					wtsheet.write(i, index_year, new_year)
				# print(new_filepath)
				wtsheet.write(i, index_filename, new_filepath)
				wtsheet.write(i, index_filesize, new_filesize)
				if index_publication_date != 0:
					wtsheet.write(i, index_publication_date, new_publication_date)
			filename = excel_file.split(".")[0] + '.new.xls'
			print('success generate: ' + filename)
			wtbook.save(filename)
	elif report_type == 'huibian':
		if 'filename' in t_keys:
			index_filename, nrows, ncols = getIndexByTitle(excel_file, title='filename')
		else:
			index_filename, nrows, ncols = getIndexByTitle(excel_file, title='FileName')

		if 'filesize' in t_keys:
			index_filesize, nrows, ncols = getIndexByTitle(excel_file, title='filesize')
		else:
			index_filesize, nrows, ncols = getIndexByTitle(excel_file, title='FileSize')

		if 'Date' in t_keys:
			index_publication_date, nrows, ncols = getIndexByTitle(excel_file, title='Date')
		else:
			index_publication_date, nrows, ncols = getIndexByTitle(excel_file, title='date')

		if(index_filename == 0 or index_filesize == 0):
			print(excel_file)
		else:
			book = xlrd.open_workbook(excel_file)
			wtbook = xlutils.copy.copy(book)
			wtsheet = wtbook.get_sheet(0)
			for i in range(1, nrows):
				if 'filename' in t_keys:
					old_filepath = table_list[i-1]['filename'].replace('\\', '/')
				else:
					old_filepath = table_list[i-1]['FileName'].replace('\\', '/')

				if old_filepath[0] == '/':
					new_filepath = filepath_in_computer + old_filepath
				else:
					new_filepath = filepath_in_computer + '/' + old_filepath

				if 'filesize' in t_keys:
					new_filesize = fileSizeChange(table_list[i-1]['filesize'])
				else:
					new_filesize = fileSizeChange(table_list[i-1]['FileSize'])

				new_publication_date = transTime(table_list[i - 1]['Date'])
				# print(new_filepath)
				wtsheet.write(i, index_filename, new_filepath)
				wtsheet.write(i, index_filesize, new_filesize)
				wtsheet.write(i, index_publication_date, new_publication_date)
			filename = excel_file.split(".")[0] + '.new.xls'
			print('success generate: ' + filename)
			wtbook.save(filename)
	else:
		pass

# 根据不同的文献类型获取cid
def getCid(report_name):
	report_list = ['IEL', 'SPIE', 'AIAA', 'IQPC', 'AD', 'DE', 'PB', 'NASA', 'DMS', 'JANES', 'ELSEVIER', 'NTIS', 'INSPEC',
	               'EI', 'AERO', '电子科技文摘库', '硕博论文库', '科技成果库', '综合数据库', '预留数据库', '自建库']
	cid = str(report_list.index(report_name) + 1)
	return cid

def excelDataChange(excel_file, report_type, report_name):
	table_list = excelTableByIndex(excel_file)
	data_list = []
	t_keys = table_list[0].keys()
	if report_type == 'QK':
		for t in table_list:
			temp_dict = {}
			if len(t['journalname']) >= 250:
				temp_dict['sid'] = getSidFromS_sourceByMeetingname(t['journalname'][:250])
			else:
				temp_dict['sid'] = getSidFromS_sourceByMeetingname(t['journalname'])
			temp_dict['cid'] = getCid(report_name)
			temp_dict['year'] = t['year']
			temp_dict['vol'] = t['volume']
			temp_dict['encryptlevel'] = '1'
			temp_dict['language'] = 'eng'
			temp_dict['docmedia'] = 'P'
			temp_dict['doi'] = t['DOI']
			if len(t['title']) > 200:
				temp_dict['mtitle'] = t['title'][0:199]
			else:
				temp_dict['mtitle'] = t['title']
			if len(t['author']) > 200:
				temp_dict['authors'] = t['author'][0:199]
			else:
				temp_dict['authors'] = t['author']
			if len(t['organ']) > 500:
				temp_dict['authorunit'] = t['organ'][0:499]
			else:
				temp_dict['authorunit'] = t['organ']
			if len(t['keyword']) > 200:
				temp_dict['keyword'] = t['keyword'][0:199]
			else:
				temp_dict['keyword'] = t['keyword']
			temp_dict['abstracts'] = t['abstract']
			temp_dict['pages'] = int(t['pages'])
			temp_dict['bepage'] = t['strpage']
			if 'filename' in t_keys:
				temp_dict['filename'] = t['filename'].split('/')[-1]
				temp_dict['filepath'] = t['filename']
			else:
				temp_dict['filename'] = t['FileName'].split('/')[-1]
				temp_dict['filepath'] = t['FileName']
			if 'filesize' in t_keys:
				temp_dict['filesize'] = t['filesize']
			else:
				temp_dict['filesize'] = t['FileSize']
			data_list.append(temp_dict)
		return data_list

	elif report_type == 'HY':
		for t in table_list:
			temp_dict = {}
			if 'Meetingname' in t_keys:
				if len(t['Meetingname']) >= 250:
					temp_dict['sid'] = getSidFromS_sourceByMeetingname(t['Meetingname'][:250])
				else:
					temp_dict['sid'] = getSidFromS_sourceByMeetingname(t['Meetingname'])
			else:
				if len(t['MeetingName']) >= 250:
					temp_dict['sid'] = getSidFromS_sourceByMeetingname(t['MeetingName'][:250])
				else:
					temp_dict['sid'] = getSidFromS_sourceByMeetingname(t['MeetingName'])

			temp_dict['cid'] = getCid(report_name)
			temp_dict['year'] = t['year']
			temp_dict['vol'] = t['MeetingVolume']
			temp_dict['encryptlevel'] = '1'
			temp_dict['language'] = 'eng'
			temp_dict['docmedia'] = 'P'
			temp_dict['doi'] = t['DOI']

			if 'Title' in t_keys:
				if len(t['Title']) > 200:
					temp_dict['mtitle'] = t['Title'][0:199]
				else:
					temp_dict['mtitle'] = t['Title']
			else:
				if len(t['title']) > 200:
					temp_dict['mtitle'] = t['title'][0:199]
				else:
					temp_dict['mtitle'] = t['title']

			if len(t['author']) > 200:
				temp_dict['authors'] = t['author'][0:199]
			else:
				temp_dict['authors'] = t['author']
			if len(t['organ']) > 500:
				temp_dict['authorunit'] = t['organ'][0:499]
			else:
				temp_dict['authorunit'] = t['organ']
			if len(t['keyword']) > 200:
				temp_dict['keyword'] = t['keyword'][0:199]
			else:
				temp_dict['keyword'] = t['keyword']

			if 'Abstract' in t_keys:
				temp_dict['abstracts'] = t['Abstract']
			else:
				temp_dict['abstracts'] = t['abstract']

			if 'pages' in t_keys:
				temp_dict['pages'] = int(t['pages'])
			elif 'Pages' in t_keys:
				temp_dict['pages'] = int(t['Pages'])
			else:
				temp_dict['pages'] = 0

			if 'strpage' in t_keys:
				temp_dict['bepage'] = t['strpage']
			elif 'strPage' in t_keys:
				temp_dict['bepage'] = t['strPage']
			else:
				temp_dict['bepage'] = ''
			if 'filename' in t_keys:
				temp_dict['filename'] = t['filename'].split('/')[-1]
				temp_dict['filepath'] = t['filename']
			else:
				temp_dict['filename'] = t['FileName'].split('/')[-1]
				temp_dict['filepath'] = t['FileName']

			if 'filesize' in t_keys:
				temp_dict['filesize'] = t['filesize']
			else:
				temp_dict['filesize'] = t['FileSize']
			data_list.append(temp_dict)
		return data_list
	elif report_type == 'report':
		for t in table_list:
			temp_dict = {}
			if 'Technical Report' in t['TitleNote']:
				temp_dict['sid'] = getSidFromS_sourceByMeetingname('Technical Report')
			else:
				temp_dict['sid'] = getSidFromS_sourceByMeetingname(t['TitleNote'])

			temp_dict['cid'] = getCid(report_name)
			temp_dict['year'] = t['year']
			temp_dict['vol'] = ''
			temp_dict['encryptlevel'] = '1'
			temp_dict['language'] = 'eng'
			temp_dict['docmedia'] = 'R'
			temp_dict['doi'] = ''

			if 'Title' in t_keys:
				if len(t['Title']) > 200:
					temp_dict['mtitle'] = t['Title'][0:199]
				else:
					temp_dict['mtitle'] = t['Title']
			else:
				if len(t['title']) > 200:
					temp_dict['mtitle'] = t['title'][0:199]
				else:
					temp_dict['mtitle'] = t['title']

			if len(t['Author']) > 200:
				temp_dict['authors'] = t['Author'][0:199]
			else:
				temp_dict['authors'] = t['Author']
			if len(t['organ']) > 500:
				temp_dict['authorunit'] = t['organ'][0:499]
			else:
				temp_dict['authorunit'] = t['organ']
			if len(t['Keyword']) > 200:
				temp_dict['keyword'] = t['Keyword'][0:199]
			else:
				temp_dict['keyword'] = t['Keyword']

			if 'Abstract' in t_keys:
				temp_dict['abstracts'] = t['Abstract']
			else:
				temp_dict['abstracts'] = t['abstract']

			if 'pages' in t_keys:
				temp_dict['pages'] = int(t['pages'])
			elif 'Pages' in t_keys:
				temp_dict['pages'] = int(t['Pages'])
			else:
				temp_dict['pages'] = int(t['pageCount'])

			if 'strpage' in t_keys:
				temp_dict['bepage'] = t['strpage']
			elif 'strPage' in t_keys:
				temp_dict['bepage'] = t['strPage']
			else:
				temp_dict['bepage'] = ''

			if 'filename' in t_keys:
				temp_dict['filename'] = t['filename'].split('/')[-1]
				temp_dict['filepath'] = t['filename']
			else:
				temp_dict['filename'] = t['FileName'].split('/')[-1]
				temp_dict['filepath'] = t['FileName']

			if 'filesize' in t_keys:
				temp_dict['filesize'] = t['filesize']
			else:
				temp_dict['filesize'] = t['FileSize']
			data_list.append(temp_dict)
		return data_list
	elif report_type == 'huibian':
		for t in table_list:
			temp_dict = {}
			if 'Publication' in t_keys:
				temp_dict['sid'] = getSidFromS_sourceByMeetingname(t['Publication'])
			else:
				temp_dict['sid'] = getSidFromS_sourceByMeetingname(t['publication'])

			temp_dict['cid'] = getCid(report_name)
			temp_dict['year'] = t['year']
			temp_dict['vol'] = ''
			temp_dict['encryptlevel'] = '1'
			temp_dict['language'] = 'eng'
			temp_dict['docmedia'] = 'G'
			temp_dict['doi'] = ''

			if 'Title' in t_keys:
				if len(t['Title']) > 200:
					temp_dict['mtitle'] = t['Title'][0:199]
				else:
					temp_dict['mtitle'] = t['Title']
			else:
				if len(t['title']) > 200:
					temp_dict['mtitle'] = t['title'][0:199]
				else:
					temp_dict['mtitle'] = t['title']

			temp_dict['authors'] = ''
			temp_dict['authorunit'] = ''
			temp_dict['keyword'] = ''
			temp_dict['abstracts'] = t['Description']

			if 'pages' in t_keys:
				temp_dict['pages'] = int(t['pages'])
			elif 'Pages' in t_keys:
				temp_dict['pages'] = int(t['Pages'])
			else:
				temp_dict['pages'] = int(t['pageCount'])

			if 'strpage' in t_keys:
				temp_dict['bepage'] = t['strpage']
			elif 'strPage' in t_keys:
				temp_dict['bepage'] = t['strPage']
			else:
				temp_dict['bepage'] = ''

			if 'filename' in t_keys:
				temp_dict['filename'] = t['filename'].split('/')[-1]
				temp_dict['filepath'] = t['filename']
			else:
				temp_dict['filename'] = t['FileName'].split('/')[-1]
				temp_dict['filepath'] = t['FileName']

			if 'filesize' in t_keys:
				temp_dict['filesize'] = t['filesize']
			else:
				temp_dict['filesize'] = t['FileSize']
			data_list.append(temp_dict)
		return data_list
	else:
		pass

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
	print(count)

	cursor.close()
	db.close()

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
	print(count)
	cursor.close()
	db.close()

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