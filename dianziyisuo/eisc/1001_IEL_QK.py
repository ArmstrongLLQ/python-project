# -*- coding: utf-8 -*-
'''
IEL 会议处理
'''
from BASE import connectDatabase, openExcel, excelTableByIndex, fileExist, getIndexByTitle, fileSizeChange
import xlutils.copy
import xlrd
from time_trans_demo import transTime
from demo2_s_source import getSidFromS_sourceByMeetingname, finalJournal

# 更新字段,然后返回一个新的excel文件，并且文件名中带有.new，之后使用新生成的.xls文件进行后面的数据库插入操作，
# 不同的excel文件字段不一样
def updateData(excel_file):
	index_filename, nrows, ncols = getIndexByTitle(excel_file, title='filename')
	index_filesize, nrows, ncols = getIndexByTitle(excel_file, title='filesize')
	index_issue_date, nrows, ncols = getIndexByTitle(excel_file, title='issueDate')
	if(index_filename == 0 or index_filesize == 0):
		print(excel_file)
	else:
		book = xlrd.open_workbook(excel_file)
		wtbook = xlutils.copy.copy(book)
		wtsheet = wtbook.get_sheet(0)
		table_list = excelTableByIndex(excel_file)
		for i in range(1, nrows):
			new_filepath = '/IELDVD/2018004/QK' + table_list[i-1]['filename'].replace('\\', '/')
			new_filesize = fileSizeChange(table_list[i-1]['filesize'])
			new_issue_date = transTime(table_list[i-1]['issueDate'])
			# print(new_filepath)
			wtsheet.write(i, index_filename, new_filepath)
			wtsheet.write(i, index_filesize, new_filesize)
			wtsheet.write(i, index_issue_date, new_issue_date)
		filename = excel_file.split(".")[0] + '.new.xls'
		print(filename)
		wtbook.save(filename)

# 根据不同的文献类型获取cid
def getCid():
	return 1

# 读取excel文件里面的数据，然后对数据进行处理，返回data_list给insertNewDataToS_data进行数据库插入操作
# 根据字段不同需要进行相应的修改
def excelDataChange(excel_file):
	table_list = excelTableByIndex(excel_file)
	data_list = []
	for t in table_list:
		temp_dict = {}
		temp_dict['sid'] = getSidFromS_sourceByMeetingname(t['journalname'])
		temp_dict['cid'] = getCid()
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
	count = 0
	for data in data_list:
		# 18个字段
		sql = """insert into s_data_1001 (`sid`,`cid`,`year`,`vol`,`encryptlevel`,`language`,`docmedia`,`doi`,`mtitle`,
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

def insertErrorData(data_list):
	db, cursor = connectDatabase()
	count = 0
	sql = 'select filename from s_data_1001'
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
				sql = """insert into s_data_1001 (`sid`,`cid`,`year`,`vol`,`encryptlevel`,`language`,`docmedia`,`doi`,`mtitle`,
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

def main():
	excel_file = 'Z:/ALLPDF/IELDVD/2018004/IEEE会议2.xlsx'
	actual_filepath = 'Z:/ALLPDF/IELDVD/2018004/HY'
	# table_list = excelTableByIndex(excel_file)

	# step1：判断文件是否存在，成功后可以将函数注释掉，也可以不注释
	# fileExist(table_list, actual_filepath)

	# step2：更新字段,然后返回一个新的excel文件，并且文件名中带有.new，之后使用新生成的.xls文件进行后面的数据库插入操作，
	# 生成新的xls文件之后将这个函数注释掉
	updateData(excel_file)

	new_excel_file = 'Z:/ALLPDF/IELDVD/2018004/IEEE期刊2.new.xls'

	# step3: 更新s_source中的数据，期刊用finalJournal，会议用finalMeeting，完成之后注释掉
	# finalJournal(new_excel_file)

	# step4：读取新生成的excel文件，然后取出需要的字段，对字段进行处理，转换成标准的格式
	# data_list = excelDataChange(new_excel_file)
	# print(len(data_list))

	# step5：将新数据插入对应的数据库表中
	# insertNewDataToS_data(data_list)
	# 根据id字段修改docid字段
	# changeDocidById()

	# step6:如果数据出错，注释第五步，执行第六步
	# insertErrorData(data_list)
	# changeDocidById()

if __name__ == '__main__':
	main()