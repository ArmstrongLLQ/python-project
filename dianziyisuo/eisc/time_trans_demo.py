# -*- coding: utf-8 -*-
'''
转换时间的格式，将英文的时间格式转换为XXXX-XX-XX
'''

import re
import datetime
from BASE import transTime

def main():
	time_list = ['September 18, 2017', '2018/02', '27 JANUARY - 1 FEBRUARY 2018', '07 3月 2018', '2018/2/15']
	for t in time_list:
		print(transTime(t))

if __name__ == '__main__':
	main()



