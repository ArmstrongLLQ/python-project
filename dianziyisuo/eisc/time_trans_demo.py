# -*- coding: utf-8 -*-
'''
转换时间的格式，将英文的时间格式转换为XXXX-XX-XX
'''

import re
import datetime

def transTime(time):
	another_time = re.search(r'\d \d \d\d\d\d|\d \d\d \d\d\d\d|\d\d \d \d\d\d\d|\d\d \d\d \d\d\d\d', time)
	if another_time:
		temp = another_time.group()
		year = temp.split(' ')[2]
		if int(temp.split(' ')[0]) > 12:
			day = temp.split(' ')[0]
			month = temp.split(' ')[1]
		else:
			month = temp.split(' ')[0]
			day = temp.split(' ')[1]
		trans_time = year + '-' + month + '-' + day
		# print(trans_time)
		return trans_time

	another_time2 = re.search(r'\d\d\d\d/\d\d', time)
	if another_time2:
		temp = another_time2.group()
		year = temp.split('/')[0]
		month = temp.split('/')[1]
		day = '1'
		trans_time = year + '-' + month + '-' + day
		# print(trans_time)
		return trans_time

	# '07 3月 2018'
	another_time3 = re.search(r'\d\d \d月 \d\d\d\d|\d\d \d\d月 \d\d\d\d', time)
	if another_time3:
		temp = another_time3.group()
		year = temp.split(' ')[2]
		month = temp.split(' ')[1].replace('月', '')
		day = temp.split(' ')[0]
		trans_time = year + '-' + month + '-' + day
		# print(trans_time)
		return trans_time

	# 2018/2/15
	another_time4 = re.search(r'\d\d\d\d/\d+/\d+', time)
	if another_time4:
		temp = another_time4.group()
		year = temp.split('/')[0]
		month = temp.split('/')[1]
		day = temp.split('/')[2]
		trans_time = year + '-' + month + '-' + day
		# print(trans_time)
		return trans_time

	# 20160202-20160203
	another_time5 = re.search(r'\d\d\d\d\d\d\d\d', time)
	if another_time5:
		temp = another_time5.group()
		year = temp[0:4]
		month = temp[4:6]
		day = temp[6:8]
		trans_time = year + '-' + month + '-' + day
		# print(trans_time)
		return trans_time

	month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
	              'November', 'December', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Sep',
	              'Oct', 'Nov', 'Dec']
	year = re.search(r'\d\d\d\d', time)
	if year:
		trans_year = year.group()
	else:
		trans_year = '2018'
	month = re.search(r'[a-zA-Z]+', time)
	if month:
		trans_month = month.group()
		trans_month = trans_month.capitalize()
		# print(trans_month)
		if trans_month == 'Sept':
			trans_month = 'Sep'
		if trans_month not in month_list:
			trans_month = '1'
			trans_day = '1'
			trans_time = trans_year + '-' + trans_month + '-' + trans_day
			return trans_time
		day = re.search(r'\d\d-|\d\d |\d-|\d |\d\d,|\d,', time)
		if day:
			trans_day = re.search(r'\d\d|\d', day.group()).group()
		else:
			trans_day = '1'
		time_temp = trans_year + ' ' + trans_month + ' ' + trans_day
		# print(time)
		try:
			time_format = datetime.datetime.strptime(time_temp, '%Y %b %d')
		except:
			time_format = datetime.datetime.strptime(time_temp, '%Y %B %d')
		trans_time = str(time_format.year) + '-' + str(time_format.month) + '-' + str(time_format.day)
		return trans_time
	else:
		trans_month = '1'
		trans_day = '1'
		trans_time = trans_year + '-' + trans_month + '-' + trans_day
		return trans_time

def main():
	time_list = ['2017/06/15', '20160202-20160203']
	for t in time_list:
		print(transTime(t))

if __name__ == '__main__':
	main()



