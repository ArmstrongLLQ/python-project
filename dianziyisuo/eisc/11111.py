# -*- coding: utf-8 -*-

from BASE import connectDatabase, excelTableByIndex

def main():
	db, cursor = connectDatabase()
	new_excel_file = 'Z:/ALLPDF/SPIE-FULLTXT/2018004/SPIE会议.new.xls'
	table_list = excelTableByIndex(new_excel_file)
	print(len(table_list))
	for t in table_list:
		# print(t['filename'])
		confdate = t['MeetingDate']
		sourcename = t['MeetingName']
		sql = 'update s_source set pubdate="%s" where sourcename="%s"' % ('0000-00-00', sourcename)
		# print(sql)
		try:
			cursor.execute(sql)
			db.commit()
		except Exception as e:
			print(e)
			db.rollback()
	cursor.close()
	db.close()

if __name__ == '__main__':
	main()

