# -*- coding: utf-8 -*-
'''
将文献数据导入数据库，导入之前进行清洗转换工作
'''
from BASE import openExcel, excelTableByIndex, connectDatabase
from time_trans_demo import transTime

# 从s_source表中取出sourcename字段
def getSourcenameFromEisc_data():
	db, cursor = connectDatabase()
	sql = 'select sourcename from s_source'
	source_list = []
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			source_list.append(row[0])
	except Exception as e:
		print(e)
	cursor.close()
	db.close()
	return source_list

# 从excel表格中将meeting的数据取出来，然后去重，得到meeting_list，下一步将meeting_list的内容存入s_source中
def getMeetinglist(table_list):
	meeting_list_temp = []
	for i in table_list:
		meeting_dict = {}
		i_keys = i.keys()
		if 'MeetingName' in i_keys:
			meeting_dict['Meetingname'] = i['MeetingName']
		else:
			meeting_dict['Meetingname'] = i['Meetingname']
		if 'MeetingDate' in i_keys:
			meeting_dict['MeetingDate'] = transTime(i['MeetingDate'])
		else:
			meeting_dict['MeetingDate'] = transTime(i['Meetingdate'])
		meeting_dict['MeetingAddress'] = i['MeetingAddress']
		if 'isbn' in i_keys:
			meeting_dict['ISBN'] = i['isbn']
		else:
			meeting_dict['ISBN'] = i['ISBN']
		meeting_dict['publicationDate'] = transTime(i['publicationDate'])
		meeting_list_temp.append(meeting_dict)
	meeting_list = []
	meetingname_list = []
	for m in meeting_list_temp:
		if m['Meetingname'] not in meetingname_list:
			meetingname_list.append(m['Meetingname'])
			meeting_list.append(m)
	return meeting_list

def getJournalList(table_list):
	journal_list_temp = []
	for i in table_list:
		journal_dict = {}
		i_keys = i.keys()
		if 'journalname' in i_keys:
			journal_dict['journalname'] = i['journalname']
		else:
			journal_dict['journalname'] = i['JournalName']
		if 'issn' in i_keys:
			journal_dict['issn'] = i['issn']
		else:
			journal_dict['issn'] = i['ISSN']
		journal_list_temp.append(journal_dict)
	journal_list = []
	journalname_list = []
	for j in journal_list_temp:
		if j['journalname'] not in journalname_list:
			journalname_list.append(j['journalname'])
			journal_list.append(j)
	return journal_list

# 将s_source表里面原来不存在的meeting插入
def insertS_sourceByMeeting(meeting_list, source_list):
	db, cursor = connectDatabase()
	for m in meeting_list:
		if m['Meetingname'] not in source_list:
			try:
				sql = 'insert into s_source (`collectiontunit`,`isbn`,`sourcename`,`pubdate`,`confaddress`,`confdate`,`doctype`) \
	VALUES ("%s","%s","%s","%s","%s","%s","%s")' % \
				      ('电子一所文献中心', m['ISBN'], m['Meetingname'], m['publicationDate'], m['MeetingAddress'],
				       m['MeetingDate'], 'C')
				# print(sql)
				cursor.execute(sql)
				db.commit()
			except Exception as e:
				print(e)
				db.rollback()
	cursor.close()
	db.close()

# 将s_source表里面原来不存在的journal插入
def insertS_sourceByJournal(journal_list, source_list):
	db, cursor = connectDatabase()
	for j in journal_list:
		if j['journalname'] not in source_list:
			try:
				sql = 'insert into s_source (`collectiontunit`,`issn`,`sourcename`,`doctype`) VALUES ("%s","%s","%s","%s")' % \
				      ('电子一所文献中心', j['issn'], j['journalname'], 'J')
				# print(sql)
				cursor.execute(sql)
				db.commit()
			except Exception as e:
				print(e)
				db.rollback()
	cursor.close()
	db.close()

# 通过会议名查询会议对应的s_id
def getSidFromS_sourceByMeetingname(meeting_name):
	db, cursor = connectDatabase()
	sql = 'select s_id from s_source where sourcename="%s"' % meeting_name
	# print(sql)
	try:
		cursor.execute(sql)
		s_id = cursor.fetchone()
	except Exception as e:
		print(e)
	cursor.close()
	db.close()
	return s_id[0]

def finalMeeting(excel_filename):
	source_list = getSourcenameFromEisc_data()
	table_list = excelTableByIndex(excel_filename)
	meeting_list = getMeetinglist(table_list)
	insertS_sourceByMeeting(meeting_list, source_list)

def finalJournal(excel_filename):
	source_list = getSourcenameFromEisc_data()
	table_list = excelTableByIndex(excel_filename)
	journal_list = getJournalList(table_list)
	insertS_sourceByJournal(journal_list, source_list)

#IEEE Transactions on Energy Conversion
# '0885-1-1'
def main():
	excel_filename = 'D:/lilanqing/Data/wenxian/2018004/IEEE期刊.xlsx'

	# finalJournal(excel_filename)
	sid = getSidFromS_sourceByMeetingname('IEEE Transactions on Energy Conversion')
	print(sid)

if __name__ == '__main__':
	main()
