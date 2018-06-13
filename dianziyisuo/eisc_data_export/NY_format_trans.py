# -*- coding: utf-8 -*-
'''
能源报告数据格式转换
'''

import xlrd
import xlwt
import xlutils.copy

def openExcel(filename):
	try:
		data = xlrd.open_workbook(filename)
		return data
	except Exception as e:
		print("openExcel Error:" + str(e))

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

# 原字段
# ID,MTitle,STitle,Author,ACompany,KeyWord,FreeWord,Subject,Abstract,Notes,Pages,MPubName,
# SPubName,PYear,PVol,PIssue,PDate,PUnit,PType,Catalog,Nums_A,Nums_B,Nums_C,Nums_D,Nums_E,FileName,FileSize,FilePath
# 目标字段
# ID,NewsNUM,Title,Authors,Organ,ReportNum,Explain,Pubdate,Pages,Language,Keywords,FreeWords,Abstract,Subject,
# Panfu,Mulu,PY,HasPDF,PDFSize
def transFormat(data_list):
	trans_data_list = []
	for data in data_list:
		try:
			trans_data = [data['ID'], '', data['MTitle'], data['Author'], data['ACompany'], '',
			              '', data['PDate'], data['Pages'], '', data['KeyWord'], '', data['Abstract'], data['Subject'],
			              '', data['Filepath'], data['PYear'], data['FileName'], data['FileSize']]
		except:
			trans_data = [data['ID'], '', data['MTitle'], data['Author'], data['ACompany'], '',
			              '', data['PDate'], data['Pages'], '', data['KeyWord'], '', data['Abstract'], data['Subject'],
			              '', data['FilePath'], data['PYear'], data['FileName'], data['FileSize']]
		# trans_data['ID'] = data['ID']
		# trans_data['NewsNUM'] = ''
		# trans_data['Title'] = data['STitle']
		# trans_data['Authors'] = data['Author']
		# trans_data['Organ'] = data['ACompany']
		# trans_data['ReportNum'] = data['FileName']
		# trans_data['Explain'] = data['']
		# trans_data['Pubdate'] = data['PDate']
		# trans_data['Pages'] = data['Pages']
		# trans_data['Language'] = ''
		# trans_data['Keywords'] = data['KeyWord']
		# trans_data['FreeWords'] = ''
		# trans_data['Abstract'] = data['Abstract']
		# trans_data['Subject'] = data['Subject']
		# trans_data['Panfu'] = ''
		# trans_data['Mulu'] = data['FilePath']
		# trans_data['PY'] = data['PYear']
		# trans_data['HasPDF'] = '1'
		# trans_data['PDFSize'] = data['FileSize']

		trans_data_list.append(trans_data)
	return trans_data_list

def writeExcel(format_excel_file, trans_data_list, new_filename):
	book = xlrd.open_workbook(format_excel_file)
	wtbook = xlutils.copy.copy(book)
	wtsheet = wtbook.get_sheet(0)
	for i in range(len(trans_data_list)):
		for j in range(len(trans_data_list[i])):
			wtsheet.write(i+1, j, trans_data_list[i][j])
	wtbook.save('D:\\lilanqing\\Project_local\\python\\dianziyisuo\\eisc_data_export\\要更改的能源报告数据表\\data\\' + new_filename + '.xls')


def main():
	excel_file_list = ['2014001', '2015001', '2015002', '2016001', '2016002',
	                   '2016003', '2017001', '2017002', '2017003', '2017004']
	for excel_file_num in excel_file_list:
		excel_file = 'D:\\lilanqing\\Project_local\\python\\dianziyisuo\\eisc_data_export\\要更改的能源报告数据表\\data\\' + excel_file_num + '.xlsx'
		data_list = excelTableByIndex(excel_file)

		print(len(data_list))

		trans_data_list = transFormat(data_list)
		format_excel_file = 'D:\\lilanqing\\Project_local\\python\\dianziyisuo\\eisc_data_export\\要更改的能源报告数据表\\data\\DE2014001.xlsx'
		writeExcel(format_excel_file, trans_data_list, excel_file_num)


if __name__ == '__main__':
	main()