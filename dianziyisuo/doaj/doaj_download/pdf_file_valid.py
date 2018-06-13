# -*- coding: utf-8 -*-
'''
判断pdf文件是否有效
'''

import os
from PyPDF2 import PdfFileReader

def isValidPDF(file_path):
	is_valid = True
	try:
		reader = PdfFileReader(file_path)
		if reader.getNumPages() < 1:
			is_valid = False
	except Exception as e:
		is_valid = False
		print(e)
	return is_valid

def getAllFilename(path):
	pdf_file_list = []
	for i in os.walk(path):
		pdf_file_list = i[2]
	return pdf_file_list

def main():
	pdf_file_list = getAllFilename('./pdf_download')
	# print(pdf_file_list)
	count = 0
	valid_pdf_file_list = []
	for pdf_file in pdf_file_list:
		is_valid = isValidPDF('./pdf_download/' + pdf_file)
		if is_valid:
			valid_pdf_file_list.append(pdf_file)
			count += 1
		# 删除出错的pdf文件
		if not is_valid:
			print(pdf_file)
			os.remove('./pdf_download/' + pdf_file)
	print(len(valid_pdf_file_list))
	print(count)
	# f_log = open('log.txt', 'a+')
	# for file in valid_pdf_file_list:
	# 	f_log.writelines(file)



if __name__ == '__main__':
	main()