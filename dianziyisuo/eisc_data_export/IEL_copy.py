# -*- coding: utf-8 -*-
'''
IEL数据copy
'''

import os
import shutil
from IEL_format_trans import connectDatabase

def getSidFromS_sourceByISSN(issn_list):
	db, cursor = connectDatabase()
	sid_list = []
	for issn in issn_list:
		sql = 'select s_id from s_source where issn="%s"' % issn
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			for r in results:
				# print(r)
				sid_list.append(r[0])
		except Exception as e:
			print('getSidFromS_sourceByISSN error' + str(e))
	cursor.close()
	db.close()
	return sid_list

def getFilepathFromSdataBySidAndTime(sid_list, time):
	db, cursor = connectDatabase()
	filepath_list = []
	for sid in sid_list:
		sql = 'select filepath from s_data_1001 where sid="%s"' % sid
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			for r in results:
				if time in r[0]:
					# print(r[0])
					filepath_list.append(r[0].split('/')[-3] + '/' + r[0].split('/')[-2])
		except Exception as e:
			print('getFilepathFromSdataBySidAndTime error' + str(e))
	filepath_list = list(set(filepath_list))
	cursor.close()
	db.close()
	return filepath_list

def main():
	issn_str = '''0018-9375/1541-1672/0018-9235/1051-8223/0018-9286/0272-1708/1949-3053/0278-0046/0018-9529/1949-3029/
	1045-9219/0090-6778/0093-9994/0885-8950/1540-7985/0885-8993/0018-9456/1057-7122/1057-7130/1089-7798/1943-0620/
	1077-2618/0741-3106/0163-6804/1540-7977/0885-8969/0885-8950/1755-4543/1751-8660/1752-1416/2168-6777/
	0885-8977/1751-8660/0733-8716/1673-5447/1751-8628/2162-2337/1229-2370'''.replace('\n\t', '')
	issn_list = issn_str.split('/')
	# getDataFromS_sourceByISSN(issn_list)
	sid_list = getSidFromS_sourceByISSN(issn_list)
	# print(sid_list)
	time_list = ['2016009', '2016010', '2016011', '2016012', '2017001', '2017002', '2017003', '2017004', '2017005',
	             '2017006', '2017007', '2017008', '2017009', '2017010', '2017011', '2017012', '2018001', '2018002',
	             '2018003']
	for time in time_list:
		filepath_list = getFilepathFromSdataBySidAndTime(sid_list, time)
		print(filepath_list)
		for f in filepath_list:
			# if not os.path.exists('IEL期刊/'+time):
			# 	os.mkdir('IEL期刊/'+time)
			shutil.copytree('Z:/ALLPDF/IELDVD/'+time+'/'+f, './IEL期刊/'+time +'/'+ f)
	# excel_file = 'D:\\lilanqing\\Project_local\\python\\dianziyisuo\\eisc_data_export\\IEL期刊\\IEL-Journal-201609.xls'
	# data_list = excelTableByIndex(excel_file)
	# print(len(data_list))
	# selectDataByFilename(data_list)
	# 	shutil.copytree('d:/temp', 'c:/temp/')
if __name__ == '__main__':
	main()