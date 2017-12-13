import os
# 将清洗后的文件进行合并成一个xls文件

def get_filelist_by_dir(dir):
	filelist = []
	for root, dirs, files in os.walk(dir):
		for file in files:
			if os.path.splitext(file)[1] == '.xls':
				filelist.append(os.path.join(root, file))
	return filelist

def get_new_excel_file(filelist):
	new_filelist = []
	for file in filelist:
		if(file.split('.')[1] == 'new'):
			new_filelist.append(file)
	return new_filelist

# 首先查找默认文件夹下有多少文档需要整合

from numpy import *

def main():
	dir = 'G:\\全文库\\excel\\2016\\SAMPE2016'
	filelist = get_filelist_by_dir(dir)
	filelist = get_new_excel_file(filelist)

	ge = len(filelist)
	print(ge)

	# 实现读写数据
	# 下面是将所有文件读数据到三维列表cell[][][]中（不包含表头）
	import xlrd

	#读取表头
	bk = xlrd.open_workbook(filelist[0])
	try:
		sh = bk.sheet_by_name("Sheet1")
	except Exception as e:
		print(e)
	nrows = sh.nrows
	ncols = sh.ncols
	biaotou = []
	for m in range(ncols):
		biaotou.append(sh.cell(0,m).value)

	print(biaotou)

	matrix = []

	for i in range(ge):
		matrix.append([])
		fname = filelist[i]
		bk = xlrd.open_workbook(fname)
		try:
			sh = bk.sheet_by_name("Sheet1")
		except:
			print("在文件%s中没有找到sheet1，读取文件数据失败,要不你换换表格的名字？" % fname)
		nrows1 = sh.nrows
		ncols1 = sh.ncols
		try:
			for j in range(1, nrows1):
				matrix[i].append([])
				for k in range(0, ncols1):
					matrix[i][j-1].append(sh.cell(j, k).value)
		except Exception as e:
			print(e)


	# 下面是写数据到新的表格test.xls中哦
	import xlwt

	filename = xlwt.Workbook()

	def func_aaa(filename, sheet_num):
		sheet = filename.add_sheet("Sheet" + str(sheet_num))
		# 下面是把表头写上
		for i in range(0, len(biaotou)):
			sheet.write(0, i, biaotou[i])
		return sheet

	sheet_num = 1
	sheet = func_aaa(filename, sheet_num)
	# 求和前面的文件一共写了多少行
	zh = 1
	for i in range(ge):
		for j in range(len(matrix[i])):
			for k in range(len(matrix[i][j])):
				sheet.write(zh, k, matrix[i][j][k])
			zh = zh + 1
			if zh >= 60000:
				sheet_num += 1
				sheet = func_aaa(filename, sheet_num)
				zh = 1

	print("我已经将%d个文件合并成1个文件，并命名为%s.xls.快打开看看正确不？" % (ge, 'final'))
	filename.save( "G:\\全文库\\excel\\2016\\SAMPE2016\\SAMPE2016.total.xls")

if __name__=="__main__":
	main()










