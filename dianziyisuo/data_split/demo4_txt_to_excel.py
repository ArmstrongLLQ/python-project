# 将txt文件转换为xls文件
import os
import xlwt

def get_filelist_by_dir(dir):
	filelist = []
	for root, dirs, files in os.walk(dir):
		for file in files:
			if os.path.splitext(file)[1] == '.txt':
				filelist.append(os.path.join(root, file))
	return filelist

# 读取txt文件内容，存入列表
def getBiaotou(filelist):
	biaotou = []
	total_data = []
	code = 'gbk'
	code = 'utf-8'
	for file in filelist:
		f_old = open(file, 'r', encoding=code)
		lines = f_old.readlines()
		record_index = []
		for i in range(len(lines)):
			if 'RECORD' in lines[i]:
				record_index.append(i)

		for j in range(len(record_index) - 1):
			data_dic = {}
			for k in range(record_index[j] + 1, record_index[j + 1]):
				if lines[k] != '\n':
					try:
						line_temp = lines[k].replace('\n', '')
						if len(line_temp) >= 30000:
							line_temp = line_temp[0:30000]
						temp = line_temp.split(':', 1)
						data_dic[temp[0]] = temp[1]
					except Exception as e:
						pass
			total_data.append(data_dic)

	for key in total_data[0].keys():
		biaotou.append(key)
	return biaotou, total_data

def func_aaa(excel_file, biaotou, sheet_num):
	sheet = excel_file.add_sheet("Sheet" + str(sheet_num))
	# 下面是把表头写上
	for i in range(0, len(biaotou)):
		sheet.write(0, i, biaotou[i])
	return sheet


def save_excel(total_data, biaotou, filename):
	excel_file = xlwt.Workbook()
	sheet_num = 1
	sheet = func_aaa(excel_file, biaotou, sheet_num)
	# 求和前面的文件一共写了多少行
	zh = 1
	file_num = 0
	for data in total_data:
		for key, i in zip(biaotou, range(len(biaotou))):
			try:
				sheet.write(zh, i, data[key])
			except Exception as e:
				pass
		zh = zh + 1
		if zh>=60000:
			sheet_num += 1
			sheet = func_aaa(excel_file,biaotou, sheet_num)
			if sheet_num >= 6:
				file_num += 1
				newfilename = filename + str(file_num)
				excel_file.save(newfilename + '.xls')
				excel_file = xlwt.Workbook()
				sheet_num = 1
				sheet = func_aaa(excel_file, biaotou, sheet_num)
			zh = 1
	excel_file.save(filename + '.final.xls')

def main():
	# filelist = get_filelist_by_dir('G:\\全文库\\txt\\2016\\ASME2016')
	filename = 'Ebsco'
	# print(filelist)
	filelist = ['G:\\全文库\\txt\\2017\\201710\\Ebsco\\Ebsco.total.txt']
	biaotou, total_data = getBiaotou(filelist)
	print(len(total_data))

	save_excel(total_data, biaotou, filename)

if __name__ == '__main__':
	main()



