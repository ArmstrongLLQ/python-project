# -*- coding: utf-8 -*-

# 将原来的只读xls文件转换为兼容文件，然后将新文件的相对路径字段进行清洗
import  xdrlib ,sys
import xlrd
import xlutils.copy
import os

def open_excel(file):
	try:
		data = xlrd.open_workbook(file)
		return data
	except Exception as e:
		print(str(e))
		
#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file,colnameindex=0,by_index=0):
	data = open_excel(file)
	table = data.sheets()[by_index]
	nrows = table.nrows #行数
	ncols = table.ncols #列数
	colnames =  table.row_values(colnameindex) #某一行数据
	list =[]
	for rownum in range(1,nrows):
		row = table.row_values(rownum)
		if row:
			app = {}
			for i in range(len(colnames)):
				app[colnames[i]] = row[i]
			list.append(app)
	return list

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file,colnameindex=0,by_name=u'Sheet1'):
	data = open_excel(file)
	table = data.sheet_by_name(by_name)
	nrows = table.nrows #行数
	colnames =  table.row_values(colnameindex) #某一行数据
	list =[]
	for rownum in range(1,nrows):
		row = table.row_values(rownum)
		if row:
			app = {}
			for i in range(len(colnames)):
				app[colnames[i]] = row[i]
			list.append(app)
	return list

# 获取相对路径字段的index
def get_index_by_title(file, title='相对路径'):
	data = open_excel(file)
	table = data.sheets()[0]
	nrows = table.nrows  # 行数
	ncols = table.ncols  # 列数
	colnames = table.row_values(0)  # 第一行数据

	for i in range(ncols):
		if(colnames[i] == title):
			return i, nrows, ncols
	return 0, 0, 0

# 获取目录下面所有xls文件的文件列表
def get_filelist_by_dir(dir):
	filelist = []
	for root, dirs, files in os.walk(dir):
		for file in files:
			if os.path.splitext(file)[1] == '.xls':
				filelist.append(os.path.join(root, file))
	return filelist
	# xls_filelist = []
	# for row in filelist:
	# 	temp = row.replace('\\', '/')
	# 	xls_filelist.append(temp)

# 删除另存的可写文件
def delete_file(filelist):
	for file in filelist:
		if (file.split('.')[1] == 'new'):
			os.remove(file)

# 将只读文件另存为为可写文件
def readonly_file_to_write_file(filelist):
	for file in filelist:
		print(file)
		book = xlrd.open_workbook(file)
		wtbook = xlutils.copy.copy(book)
		wtsheet = wtbook.get_sheet(0)
		filename = file.split(".")[0] + '.new.xls'
		wtbook.save(filename)

# 更新相对路径字段
def update_data(filelist):
	for file in filelist:
		if(file.split('.')[1] == 'new'):
			index, nrows, ncols = get_index_by_title(file)
			if(index == 0):
				print(file)
			else:
				book = xlrd.open_workbook(file)
				wtbook = xlutils.copy.copy(book)
				wtsheet = wtbook.get_sheet(0)
				table_list = excel_table_byindex(file)
				for i in range(1, nrows):
					change_data = '全文库/excel/2016/' + table_list[i-1]['相对路径'].split('/', 1)[1]
					wtsheet.write(i, index, change_data)
				filename = file#.split(".")[0] + '.new.xls'
				#print(filename)
				wtbook.save(filename)

def main():
	#tables = excel_table_byindex('AAS2016.xls')
	filelist = get_filelist_by_dir('G:\\全文库\\excel\\2016\\ASTM2016\\STP1585')

	# 将只读文件另存为为可写文件
	# readonly_file_to_write_file(filelist)

	# 删除另存的可写文件
	# delete_file(filelist)

	# 更新相对路径字段
	update_data(filelist)

if __name__=="__main__":
	main()


