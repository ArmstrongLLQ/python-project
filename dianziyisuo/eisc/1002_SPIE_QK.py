# -*- coding: utf-8 -*-
'''
IEL 会议处理
'''
from BASE import excelTableByIndex, fileExist, updateData, excelDataChange, finalJournal
from BASE import insertErrorData, changeDocidById, insertNewDataToS_data

def main():
	excel_file = 'Z:/ALLPDF/SPIE-FULLTXT/2018004/SPIE期刊2.xlsx'
	actual_filepath = 'Z:/ALLPDF/SPIE-FULLTXT/2018004/QK'
	table_list = excelTableByIndex(excel_file)
	report_type = 'QK'
	report_name = 'SPIE'
	filepath_in_computer = '/SPIE-FULLTXT/2018004/QK'
	new_excel_file = 'Z:/ALLPDF/SPIE-FULLTXT/2018004/SPIE期刊2.new.xls'

	# step1：判断文件是否存在，成功后可以将函数注释掉，也可以不注释
	# fileExist(table_list, actual_filepath)

	# step2：更新字段,然后返回一个新的excel文件，并且文件名中带有.new，之后使用新生成的.xls文件进行后面的数据库插入操作，
	# 生成新的xls文件之后将这个函数注释掉
	# updateData(excel_file, table_list, report_type, filepath_in_computer)

	# step3: 更新s_source中的数据，期刊用finalJournal，会议用finalMeeting，完成之后注释掉
	# finalJournal(new_excel_file)

	# step4：读取新生成的excel文件，然后取出需要的字段，对字段进行处理，转换成标准的格式
	data_list = excelDataChange(new_excel_file, report_type, report_name)
	print(len(data_list))

	# step5：将新数据插入对应的数据库表中
	insertNewDataToS_data(data_list, report_name)
	# 根据id字段修改docid字段
	changeDocidById(report_name)

	# step6:如果数据出错，注释第五步，执行第六步
	# insertErrorData(data_list)
	# changeDocidById()

if __name__ == '__main__':
	main()