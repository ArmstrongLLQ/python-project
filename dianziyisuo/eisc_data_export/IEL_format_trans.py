# -*- coding: utf-8 -*-
'''
IEL数据格式转换
'''
from NY_format_trans import excelTableByIndex
import pymysql
import xlrd
import xlutils.copy

# 连接远程数据库
def connectDatabase( my_host="172.16.155.31", my_username="root", my_keyword="eisc15531", my_database="eisc_data"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor

def getFilenameFromExcel(data_list):
	filename_list = []
	for i in data_list:
		filename = i['filename'].split('\\')[-1]
		filename_list.append(filename)
	return filename_list

def openExcel(filename):
	try:
		data = xlrd.open_workbook(filename)
		return data
	except Exception as e:
		print(e)

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
# 0018-9375/1541-1672/0018-9235/1051-8223/0018-9286/0272-1708/1949-3053/0278-0046/0018-9529/1949-3029
# 1045-9219/0090-6778/0093-9994/0885-8950/1540-7985/0885-8993/0018-9456/1057-7122/1057-7130/1089-7798/1943-0620
# 1077-2618/0741-3106/0163-6804/1540-7977/0885-8969/0885-8950/1755-4543/1751-8660/1752-1416/2168-67770885-8977/1751-8660/0733-8716
# 1673-5447/1751-8628/2162-2337/1229-2370
def getDataFromS_sourceByISSN(issn_list):
	db, cursor = connectDatabase()
	data_list = []
	for issn in issn_list:
		sql = 'select s_id, sourcename, pubdate, pubunit from s_source where issn="%s"' % issn
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			for r in results:
				data_dict = {}
				# print(r)
				data_dict['s_id'] = r[0]
				data_dict['sourcename'] = r[1]
				data_dict['pubdate'] = r[2]
				data_dict['pubunit'] = r[3]
				data_list.append(data_dict)
		except Exception as e:
			print('getSidFromS_sourceByISSN error' + str(e))
	cursor.close()
	db.close()
	return data_list

def selectDataFromS_data(data_list):
	db, cursor = connectDatabase()
	filename_list = getFilenameFromExcel(data_list)
	for filename in filename_list:
		sql = 'select sid from s_data_1001 where filename="%s"' % filename
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			for r in results:
				print(r)
		except Exception as e:
			print('select error' + str(e))

# ID,MTitle,STitle,Author,ACompany,KeyWord,FreeWord,Subject,Abstract,Notes,Pages,MPubName,SPubName,PYear,PVol,
# PIssue,PDate,PUnit,Catalog,PType,Nums_A,Nums_B,Nums_C,Nums_D,Nums_E,FileName,FileSize,FilePath,SPages,EPages,ALLPages
def getAllDataToList(data_list, time):
	con, cursor = connectDatabase()
	all_data_list = []
	for data in data_list:
		# print(data)
		sid = data['s_id']
		sql = """select mtitle, stitle, authors, authorunit, keyword, freeword, abstracts, notes, pages, year, 
		vol, issue, filename, filesize, filepath, bepage from s_data_1001 where sid='%s'""" % sid
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			for r in results:
				all_data = {}
				if time in r[14]:
					# s_data_1001
					all_data['MTitle'] = r[0]
					all_data['STitle'] = r[1]
					all_data['Author'] = r[2]
					all_data['ACompany'] = r[3]
					all_data['KeyWord'] = r[4]
					all_data['FreeWord'] = r[5]
					all_data['Abstract'] = r[6]
					all_data['Notes'] = r[7]
					all_data['Pages'] = r[8]
					all_data['PYear'] = r[9]
					all_data['PVol'] = r[10]
					all_data['PIssue'] = r[11]
					all_data['FileName'] = r[12]
					all_data['FileSize'] = r[13]
					all_data['FilePath'] = r[14]
					all_data['ALLPages'] = r[15]
					# s_source
					all_data['MPubName'] = data['sourcename']
					all_data['PDate'] = data['pubdate']
					all_data['PUnit'] = data['pubunit']

					all_data_list.append(all_data)
		except Exception as e:
			print('getAllDataToList error:' + str(e))

	cursor.close()
	con.close()
	return all_data_list

def allDataListToTransDataList(all_data_list):
	trans_data_list = []
	for id, all_data in zip(range(len(all_data_list)), all_data_list):
		trans_data = [id+1, all_data['MTitle'], all_data['STitle'], all_data['Author'], all_data['ACompany'], all_data['KeyWord'],
		              all_data['FreeWord'], '', all_data['Abstract'], all_data['Notes'], all_data['Pages'], all_data['MPubName'],
		              '', all_data['PYear'], all_data['PVol'], all_data['PIssue'], all_data['PDate'], all_data['PUnit'], '', '',
		              '', '', '', '', '', all_data['FileName'], all_data['FileSize'], all_data['FilePath'], '', '', all_data['ALLPages']]
		trans_data_list.append(trans_data)
	return trans_data_list

def writeExcel(format_excel_file, trans_data_list, new_filename):
	book = xlrd.open_workbook(format_excel_file)
	wtbook = xlutils.copy.copy(book)
	wtsheet = wtbook.get_sheet(0)
	for i in range(len(trans_data_list)):
		for j in range(len(trans_data_list[i])):
			wtsheet.write(i+1, j, trans_data_list[i][j])
	wtbook.save('D:\\lilanqing\\Project_local\\python\\dianziyisuo\\eisc_data_export\\IEL期刊\\new\\' + new_filename + '.xls')

def main():
	issn_str = '''0018-9375/1541-1672/0018-9235/1051-8223/0018-9286/0272-1708/1949-3053/0278-0046/0018-9529/1949-3029/
	1045-9219/0090-6778/0093-9994/0885-8950/1540-7985/0885-8993/0018-9456/1057-7122/1057-7130/1089-7798/1943-0620/
	1077-2618/0741-3106/0163-6804/1540-7977/0885-8969/0885-8950/1755-4543/1751-8660/1752-1416/2168-6777/
	0885-8977/1751-8660/0733-8716/1673-5447/1751-8628/2162-2337/1229-2370'''.replace('\n\t', '')
	issn_list = issn_str.split('/')
	# getDataFromS_sourceByISSN(issn_list)
	data_list = getDataFromS_sourceByISSN(issn_list)
	# print(data_list)
	time_list = ['2016009', '2016010', '2016011', '2016012', '2017001', '2017002', '2017003', '2017004', '2017005',
	             '2017006', '2017007', '2017008', '2017009', '2017010', '2017011', '2017012', '2018001', '2018002',
	             '2018003']
	for time in time_list:
		all_data_list = getAllDataToList(data_list, time)
		# print(all_data_list)
		trans_data_list = allDataListToTransDataList(all_data_list)
		format_excel_file = 'D:\\lilanqing\\Project_local\\python\\dianziyisuo\\eisc_data_export\\外文期刊格式.xlsx'
		writeExcel(format_excel_file, trans_data_list, time)
	# filepath_list = getFilepathFromSdataBySidAndTime(sid_list, time)
	# print(filepath_list)
	# excel_file = 'D:\\lilanqing\\Project_local\\python\\dianziyisuo\\eisc_data_export\\IEL期刊\\IEL-Journal-201609.xls'
	# data_list = excelTableByIndex(excel_file)
	# print(len(data_list))
	# selectDataByFilename(data_list)
if __name__ == '__main__':
	main()