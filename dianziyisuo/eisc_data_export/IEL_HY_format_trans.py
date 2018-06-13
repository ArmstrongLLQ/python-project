# -*- coding: utf-8 -*-
'''
IEL会议数据格式转换
'''
import pymysql
import xlrd
import xlutils.copy
import shutil
import os
# 连接远程数据库
def connectDatabase( my_host="172.16.155.31", my_username="root", my_keyword="eisc15531", my_database="eisc_data"):
	# 打开数据库连接
	db = pymysql.connect(my_host, my_username, my_keyword, my_database, charset = "utf8")
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	return db, cursor

def getHYListFromTxt(txt_file):
	f = open(txt_file, 'r')
	hy_list = f.readlines()

	for i in range(len(hy_list)):
		hy_list[i] = hy_list[i].replace('\n', '')
	return hy_list

def getSidFromS_sourceByHYName(hy_list):
	con, cursor = connectDatabase()
	sid_list = []
	for hy in hy_list:
		sql = 'select s_id from s_source where sourcename="%s"' % hy
		# print(sql)
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			for r in results:
				sid_list.append(r[0])
		except Exception as e:
			print('getSidFromS_sourceByHYName error:' + str(e))
	cursor.close()
	con.close()
	return sid_list

def getDataFromS_sourceByHYName(hy_list):
	db, cursor = connectDatabase()
	data_list = []
	for hy in hy_list:
		sql = 'select * from s_source where sourcename="%s"' % hy
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			for r in results:
				data_dict = {}
				# print(r)
				data_dict['s_id'] = r[0]
				data_dict['isbn'] = r[3]
				data_dict['issn'] = r[4]
				data_dict['sourcename'] = r[7]
				data_dict['pubunit'] = r[10]
				data_dict['pubadress'] = r[11]
				data_dict['pubdate'] = r[12]
				data_dict['confaddress'] = r[13]
				data_dict['confdate'] = r[14]
				data_dict['doctype'] = r[15]
				data_list.append(data_dict)
		except Exception as e:
			print('getSidFromS_sourceByISSN error' + str(e))
	cursor.close()
	db.close()
	return data_list

# 光盘号,会议录名称,英文会议录名称,ISSN,CN,ISBN,年,卷,期刊基本参数,期,文件名,论文题名,论文作者,
# 作者机构,文章编号,文章属性,语种,分类号,论文摘要,论文关键词,收稿日期,基金,作者简介,英文论文题名,
# 英文论文作者,英文论文摘要,英文论文关键词,引文,期刊页码,物理页码,学会代码,代码,ZJ,COLCODE,ZJCOL,
# 专题代码,子栏目代码,专题子栏目代码,全文,发行范围,会议名称,英文会议名称,会议地点,主办单位,编者,
# 出版单位,出版日期,学会名称,专委会名称,编辑部名称,主编,内部资料否,全文否,更新日期,中英文题名,
# 复合关键词,中英文摘要,主题,旧机标关键词,OLD_SYS_VSM,来源数据库,页数,文件大小,第一责任人,中英文会议名称,
# 中英文会议录名称,DOI,专辑代码,正文快照,中英文作者,网络出版投稿时间,网络出版投稿人,原文格式,下载频次,
# 被引频次,文献标识码,文献类型标识,来源标识码,主题词,KMC分类号,语义树条码,发表时间,基金代码,作者代码,
# 机构代码,TABLENAME	表名,是否含新概念,所含新概念名称,新概念代码,概念出处,是否高下载,是否高被引,是否高他引,
# 他引频次,是否基金文献,机构作者代码,报告级别,报告级别代码,会议级别,会议级别代码,会议召开时间,栏目层次,主办单位代码,
# 论文集类型,文献作者,来源代码,FFD	SMARTS,机标关键词,SYS_VSM,出版物代码

def getAllDataToList(data_list):
	con, cursor = connectDatabase()
	all_data_list = []
	for data in data_list:
		# print(data)
		sid = data['s_id']
		sql = """select mtitle, authors, authorunit, keyword, abstracts, year, vol, issue, language, pages, doi, 
		filepath, filesize from s_data_1001 where sid='%s'""" % sid
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			for r in results:
				all_data = {}
				# s_data_1001
				all_data['论文题名'] = r[0]
				all_data['论文作者'] = r[1]
				all_data['作者机构'] = r[2]
				all_data['论文关键词'] = r[3]
				all_data['论文摘要'] = r[4]
				all_data['年'] = r[5]
				all_data['卷'] = r[6]
				all_data['期'] = r[7]
				all_data['语种'] = r[8]
				all_data['页数'] = r[9]
				all_data['DOI'] = r[10]
				all_data['文件名'] = r[11]
				all_data['文件大小'] = r[12]

				all_data['会议录名称'] = data['sourcename']
				all_data['ISSN'] = data['issn']
				all_data['ISBN'] = data['isbn']
				all_data['会议名称'] = data['sourcename']
				all_data['会议地点'] = data['confaddress']
				all_data['会议召开时间'] = data['confdate']
				all_data['出版单位'] = data['pubunit']
				all_data['出版日期'] = data['pubdate']

				all_data_list.append(all_data)
		except Exception as e:
			print('getAllDataToList error:' + str(e))

	cursor.close()
	con.close()
	return all_data_list

def allDataListToTransDataList(all_data_list, hy_format_list):
	trans_data_list = []
	for data_dict in all_data_list:
		trans_data = []
		key_index_dict = {}
		for i in range(len(hy_format_list)):
			trans_data.append('')
		for k, v in data_dict.items():
			key_index = hy_format_list.index(k)
			trans_data[key_index] = v
		trans_data_list.append(trans_data)
	return trans_data_list

def writeExcel(format_excel_file, trans_data_list, new_filename):
	book = xlrd.open_workbook(format_excel_file)
	wtbook = xlutils.copy.copy(book)
	wtsheet = wtbook.get_sheet(0)
	for i in range(len(trans_data_list)):
		for j in range(len(trans_data_list[i])):
			wtsheet.write(i+1, j, trans_data_list[i][j])
	wtbook.save('D:\\lilanqing\\Project_local\\python\\dianziyisuo\\eisc_data_export\\IEL会议\\' + new_filename + '.xls')

def getFilepathFromSdataBySid(sid_list):
	db, cursor = connectDatabase()
	filepath_list = []
	for sid in sid_list:
		sql = 'select filepath from s_data_1001 where sid="%s"' % sid
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			for r in results:
				# print(r)
				filepath_list.append(r[0])
				# path_list = r[0].split('/')
				# # print(len(path_list))
				# filepath = ''
				# for i in range(len(path_list) -1):
				# 	filepath = filepath + '/' + path_list[i]
				# filepath_list.append(filepath[1:])
				# # filepath_list.append(r[0].split('/')[-4] + '/' + r[0].split('/')[-3] + '/' + r[0].split('/')[-2])
		except Exception as e:
			print('getFilepathFromSdataBySidAndTime error' + str(e))
	filepath_list = list(set(filepath_list))
	cursor.close()
	db.close()
	return filepath_list

def mycopyfile(srcfile,dstfile):
	if not os.path.isfile(srcfile):
		print("%s not exist!"%(srcfile))
	else:
		fpath,fname=os.path.split(dstfile)    #分离文件名和路径
		if not os.path.exists(fpath):
			os.makedirs(fpath)                #创建路径
		shutil.copyfile(srcfile,dstfile)      #复制文件
		# print("copy %s -> %s"%( srcfile,dstfile))

# 光盘号,会议录名称,英文会议录名称,ISSN,CN,ISBN,年,卷,期刊基本参数,期,文件名,论文题名,论文作者,作者机构,文章编号,文章属性,语种,分类号,论文摘要,论文关键词,收稿日期,基金,作者简介,英文论文题名,英文论文作者,英文论文摘要,英文论文关键词,引文,期刊页码,物理页码,学会代码,代码,ZJ,COLCODE,ZJCOL,专题代码,子栏目代码,专题子栏目代码,全文,发行范围,会议名称,英文会议名称,会议地点,主办单位,编者,出版单位,出版日期,学会名称,专委会名称,编辑部名称,主编,内部资料否,全文否,更新日期,中英文题名,复合关键词,中英文摘要,主题,旧机标关键词,OLD_SYS_VSM,来源数据库,页数,文件大小,第一责任人,中英文会议名称,中英文会议录名称,DOI,专辑代码,正文快照,中英文作者,网络出版投稿时间,网络出版投稿人,原文格式,下载频次,被引频次,文献标识码,文献类型标识,来源标识码,主题词,KMC分类号,语义树条码,发表时间,基金代码,作者代码,机构代码,TABLENAME	表名,是否含新概念,所含新概念名称,新概念代码,概念出处,是否高下载,是否高被引,是否高他引,他引频次,是否基金文献,机构作者代码,报告级别,报告级别代码,会议级别,会议级别代码,会议召开时间,栏目层次,主办单位代码,论文集类型,文献作者,来源代码,FFD	SMARTS,机标关键词,SYS_VSM,出版物代码

def main():
	hy_list = getHYListFromTxt('HY.txt')
	# sid_list = getSidFromS_sourceByHYName(hy_list)
	# print(sid_list)
	# filepath_list = getFilepathFromSdataBySid(sid_list)
	# print(len(filepath_list))
	# for f in filepath_list:
	# 	srcfile = 'Z:/ALLPDF' + f
	# 	dstfile = './IEL会议' + f
	# 	mycopyfile(srcfile, dstfile)
	# for f in filepath_list:
	# 	shutil.copytree('Z:/ALLPDF' + f, './IEL会议' + f)
	hy_format = '光盘号,会议录名称,英文会议录名称,ISSN,CN,ISBN,年,卷,期刊基本参数,期,文件名,论文题名,论文作者,作者机构,文章编号,文章属性,语种,分类号,论文摘要,论文关键词,收稿日期,基金,作者简介,英文论文题名,英文论文作者,英文论文摘要,英文论文关键词,引文,期刊页码,物理页码,学会代码,代码,ZJ,COLCODE,ZJCOL,专题代码,子栏目代码,专题子栏目代码,全文,发行范围,会议名称,英文会议名称,会议地点,主办单位,编者,出版单位,出版日期,学会名称,专委会名称,编辑部名称,主编,内部资料否,全文否,更新日期,中英文题名,复合关键词,中英文摘要,主题,旧机标关键词,OLD_SYS_VSM,来源数据库,页数,文件大小,第一责任人,中英文会议名称,中英文会议录名称,DOI,专辑代码,正文快照,中英文作者,网络出版投稿时间,网络出版投稿人,原文格式,下载频次,被引频次,文献标识码,文献类型标识,来源标识码,主题词,KMC分类号,语义树条码,发表时间,基金代码,作者代码,机构代码,TABLENAME	表名,是否含新概念,所含新概念名称,新概念代码,概念出处,是否高下载,是否高被引,是否高他引,他引频次,是否基金文献,机构作者代码,报告级别,报告级别代码,会议级别,会议级别代码,会议召开时间,栏目层次,主办单位代码,论文集类型,文献作者,来源代码,FFD	SMARTS,机标关键词,SYS_VSM,出版物代码'
	hy_format_list = hy_format.split(',')
	# print(len(hy_format_list))
	data_list = getDataFromS_sourceByHYName(hy_list)
	# print(data_list[4])
	all_data_list = getAllDataToList(data_list)
	# print(all_data_list[1])
	trans_data_list = allDataListToTransDataList(all_data_list, hy_format_list)
	# print(trans_data_list[100])
	format_excel_file = 'D:\\lilanqing\\Project_local\\python\\dianziyisuo\\eisc_data_export\\会议格式.xlsx'
	writeExcel(format_excel_file, trans_data_list, '会议')


if __name__ == '__main__':
	main()