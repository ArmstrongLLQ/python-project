# -*- coding: utf-8 -*-
'''
将文献数据导入数据库，导入之前进行清洗转换工作
'''
import xlrd
import xlutils.copy
from file_exist_demo import openExcel,excelTableByIndex,fileSizeChange
import pymysql
from time_trans_demo import transTime

# 不同文献的目录
# /IELDVD/2018004/QK  IEEE期刊
# /IELDVD/2018004/HY IEEE会议

# 连接本地数据库
def connectDatabase( my_host="localhost", my_username="root", my_keyword="", my_database="eisc_data"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor

# # 连接远程数据库
# def connectDatabase( my_host="172.16.155.31", my_username="root", my_keyword="eisc15531", my_database="eisc_data"):
# 	# 打开数据库连接
# 	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
# 	# 使用cursor()方法获取操作游标
# 	cursor = db.cursor()
# 	return db, cursor

# 获取filename字段的index
def getIndexByTitle(file, title):
	data = openExcel(file)
	table = data.sheets()[0]
	nrows = table.nrows  # 行数
	ncols = table.ncols  # 列数
	colnames = table.row_values(0)  # 第一行数据

	for i in range(ncols):
		if(colnames[i] == title):
			return i, nrows, ncols
	return 0, 0, 0

# 更新字段,然后返回一个新的excel文件，并且文件名中带有.new，之后使用新生成的.xls文件进行后面的数据库插入操作，
# 生成新的xls文件之后将这个函数注释掉
def updateData(file):
	index_filename, nrows, ncols = getIndexByTitle(file, title='filename')
	index_filesize, nrows, ncols = getIndexByTitle(file, title='filesize')
	index_meeting_date, nrows, ncols = getIndexByTitle(file, title='MeetingDate')
	index_publication_date, nrows, ncols = getIndexByTitle(file, title='publicationDate')
	if(index_filename == 0 or index_filesize == 0):
		print(file)
	else:
		book = xlrd.open_workbook(file)
		wtbook = xlutils.copy.copy(book)
		wtsheet = wtbook.get_sheet(0)
		table_list = excelTableByIndex(file)
		for i in range(1, nrows):
			new_filepath = '/IELDVD/2018004/HY' + table_list[i-1]['filename'].replace('\\', '/')
			new_filesize = fileSizeChange(table_list[i-1]['filesize'])
			new_meeting_date = transTime(table_list[i-1]['MeetingDate'])
			new_publication_date = transTime(table_list[i-1]['publicationDate'])
			# print(new_filepath)
			wtsheet.write(i, index_filename, new_filepath)
			wtsheet.write(i, index_filesize, new_filesize)
			wtsheet.write(i, index_meeting_date, new_meeting_date)
			wtsheet.write(i, index_publication_date, new_publication_date)
		filename = file.split(".")[0] + '.new.xls'
		print(filename)
		wtbook.save(filename)

# 通过会议名查询会议对应的s_id
def getSidFromS_sourceByMeetingname(meeting_name):
	db, cursor = connectDatabase()
	sql = 'select s_id from s_source where sourcename="%s"' % meeting_name
	s_id = 0
	try:
		cursor.execute(sql)
		result = cursor.fetchone()
		s_id = result[0]
	except Exception as e:
		print(e)
	cursor.close()
	db.close()
	return s_id

# 根据不同的文献类型获取cid
def getCid():
	return 1

# 读取excel文件里面的数据，然后对数据进行处理，返回data_list给insertNewDataToS_data进行数据库插入操作
def excelDataChange(excel_file):
	table_list = excelTableByIndex(excel_file)
	data_list = []
	for t in table_list:
		temp_dict = {}
		temp_dict['sid'] = getSidFromS_sourceByMeetingname(t['Meetingname'])
		temp_dict['cid'] = getCid()
		temp_dict['year'] = t['year']
		temp_dict['vol'] = t['MeetingVolume']
		temp_dict['encryptlevel'] = '1'
		temp_dict['language'] = 'eng'
		temp_dict['docmedia'] = 'P'
		temp_dict['doi'] = t['DOI']
		temp_dict['mtitle'] = t['Title']
		temp_dict['authors'] = t['author']
		temp_dict['authorunit'] = t['organ']
		temp_dict['keyword'] = t['keyword']
		temp_dict['abstracts'] = t['Abstract']
		temp_dict['pages'] = int(t['pages'])
		temp_dict['bepage'] = t['strpage']
		temp_dict['filename'] = t['filename'].split('/')[-1]
		temp_dict['filepath'] = t['filename']
		temp_dict['filesize'] = t['filesize']
		data_list.append(temp_dict)
	return data_list


# IEEE会议字段  Title,author,organ,DOI,Abstract,keyword,strpage,Meetingname,MeetingDate,MeetingAdress,MeetingVolume
#               publicationDate,year,sISBN,ISBN,Disk,filename,filesize,pages
# s_data字段  id,docid,sid,cid,year,vol,issue,encryptlevel,language,docmedia,shelfnumber,reportnumber,doi,catalognums,
#              catalogtable,mtitle,stitle,authors,authorunit,corporateauthor,keyword,keywordtable,freeword,abstracts,
#              notes,pages,bepage,filename,filepath,filesize,
def insertNewDataToS_data(data_list):
	db, cursor = connectDatabase()
	for data in data_list:
		# 18个字段
		sql = """insert into s_data_1001 (`sid`,`cid`,`year`,`vol`,`encryptlevel`,`language`,`docmedia`,`doi`,`mtitle`,
`authors`,`authorunit`,`keyword`,`abstracts`,`pages`,`bepage`,`filename`,`filepath`,`filesize`) values 
("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")""" % (data['sid'],data['cid'],data['year'],data['vol'],
		                                                      data['encryptlevel'],data['language'],data['docmedia'],
		                                                      data['doi'],data['mtitle'],data['authors'],data['authorunit'],
		                                                      data['keyword'],data['abstracts'],data['pages'],data['bepage'],
		                                                      data['filename'],data['filepath'],data['filesize'],)
		print(sql)
		try:
			cursor.execute(sql)
			db.commit()
		except Exception as e:
			print(e)
			db.rollback()
	cursor.close()
	db.close()

def changeDocidById():
	db, cursor = connectDatabase()
	sql = 'select id from s_data_1001 where docid=0'
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for r in results:
			# print(r[0])
			id = r[0]
			docid = int('1001000' + str(id))
			sql2 = 'update s_data_1001 set docid = %d where id = %d' % (docid, id)
			# print(sql2)
			try:
				cursor.execute(sql2)
				db.commit()
			except Exception as e:
				print(e)
				db.rollback()
	except Exception as e:
		print(e)
	cursor.close()
	db.close()

def main():
	excel_filename = 'D:/lilanqing/Data/wenxian/2018004/IEEE会议.xlsx'
	# 更新字段,然后返回一个新的excel文件，并且文件名中带有.new，之后使用新生成的.xls文件进行后面的数据库插入操作，
	# 生成新的xls文件之后将这个函数注释掉
	# updateData(excel_filename)

	new_excel_file = 'D:/lilanqing/Data/wenxian/2018004/IEEE会议.new.xls'
	data_list = excelDataChange(new_excel_file)

	insertNewDataToS_data(data_list)
	changeDocidById()

if __name__ == '__main__':
	main()


