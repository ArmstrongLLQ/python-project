# -*- coding: utf-8 -*-
'''
将文献数据导入数据库，导入之前进行清洗转换工作
'''
import os
import xlrd

# 判断文件是否存在
def fileExist(filepath):
	# os.path.getsize(filepath)
	if not os.path.exists(filepath):
		print(filepath)
		return False
	return True

# 对文件大小进行转换，小于1M的用K表示
def getFileSize(filename):
	file_size = os.path.getsize(filename) / 1024
	if file_size < 1024:
		file_size = str(round(file_size)) + 'K'
	else:
		file_size = str(format(file_size / 1024, '0.2f')) + 'M'
	return file_size

#
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

def main():
	excel_filename = 'D:/lilanqing/Data/wenxian/2018004/IEEE期刊.xlsx'
	table_list = excelTableByIndex(excel_filename)

	for i in table_list:
		# print(i)
		temp = 'D:/lilanqing/Data/wenxian/2018004/QK' + i['filename'].replace('\\', '/')
		if fileExist(temp):
			file_size = getFileSize(temp)
			print(file_size)

	print(len(table_list))


if __name__ == '__main__':
	main()