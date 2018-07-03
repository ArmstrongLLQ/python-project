# -*- coding: utf-8 -*-

from BASE import connectDatabase, excelTableByIndex

def a():
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

def b():
	db, cursor = connectDatabase()
	for cid in range(4, 20):
		s_data_num = 's_data_' + str(int(cid) + 1000)
		sql = 'select id,docid from '+s_data_num
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			for r in results:
				# print(r[0])
				id = r[0]
				old_docid = str(r[1])
				if old_docid[:4] == '1001':
					docid = (int(cid) + 1000) * 10000000000 + int(id)
					# docid = int('1001000' + str(id))
					sql2 = 'update ' + s_data_num + ' set docid = %d where id = %d' % (docid, id)
					# print(sql2)
					try:
						cursor.execute(sql2)
						db.commit()
					except Exception as e:
						print(e)
						db.rollback()
		except Exception as e:
			print(e)
	cursor.close()
	db.close()

def main():
	b()

if __name__ == '__main__':
	main()

# 10150000994683
# 1011000000001
# 10010000000004
# 10110000000001
# 10110000099008
# 10030000133536

Z:\ALLPDF\AERO\2018006\AeroSpace201708.xls
Z:\ALLPDF\AERO\2018006
\AERO\2018006