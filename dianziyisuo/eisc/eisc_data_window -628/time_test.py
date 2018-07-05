from BASE import transTime

def main():
	time_list = ['2017/06/15', '20160202-20160203', '23 5月 2018']
	for t in time_list:
		print(transTime(t))

if __name__ == '__main__':
	main()