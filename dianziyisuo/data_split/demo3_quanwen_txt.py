import os
# 对txt文件的相对路径字段进行修改，然后将txt文件进行合并

def get_filelist_by_dir(dir):
	filelist = []
	for root, dirs, files in os.walk(dir):
		for file in files:
			if os.path.splitext(file)[1] == '.txt':
				filelist.append(os.path.join(root, file))
	return filelist

def hebing_txt(filelist):
	total_txt = []
	code = 'utf-8'
	# code = 'gbk'
	new_file = 'G:\\全文库\\txt\\2017\\201710\\Ebsco\\Ebsco.total.txt'
	for file in filelist:
		if file.split('.')[-2] == 'new':
			print(file)
			f_old = open(file, 'r', encoding=code)
			lines = f_old.readlines()
			flen = len(lines)
			for i in range(flen):
				total_txt.append(lines[i])
	with open(new_file, 'w', encoding=code) as f_new:
		f_new.writelines(total_txt)
		print('success')

def modify_txt(filelist):
	sstr = 'FILERELPATH'
	code = 'utf-8'
	# code = 'gbk'

	for file in filelist:
		new_file = file.split('.')[0] + '.new' + '.txt'
		try:
			f_old = open(file,'r',encoding=code)
			lines = f_old.readlines()
			flen = len(lines)
			for i in range(flen):
				# if lines[i] == '\n':
				# 	lines.pop(i)
				if sstr in lines[i]:
					temp = lines[i].split(':', 1)
					# lines[i] = 'FILERELPATH:\\全文库\\txt\\2016\\' + temp[-1]
					lines[i] = 'FILERELPATH:/全文库/txt/2017/201710' + temp[-1]

			with open(new_file, 'w',  encoding=code) as f_new:
				f_new.writelines(lines)

		except Exception as e:
			print(e)

def change_encode(filelist):
	for file in filelist:
		new_file = file.split('.')[0] + '.new' + '.txt'
		try:
			f = open(file, 'r', encoding='gbk')
			lines = f.readlines()
			# print(lines)
			flen = len(lines)
			new_lines = []
			# for i in range(flen):
				# temp_new_line = lines[i].decode('utf-8')
				# new_lines.append(temp_new_line)
			# print(new_lines)
			with open(new_file, 'w',  encoding='gbk') as f1:
				f1.writelines(lines)

		except Exception as e:
			print(e)

def delete_new_file(filelist):
	for file in filelist:
		if (file.split('.')[1] == 'new'):
			os.remove(file)
			print('delete ' + file)

def main():
	dir = 'G:\\全文库\\txt\\2017\\201710'
	filelist = get_filelist_by_dir(dir)
	print(filelist)
	# change_encode(filelist)
	# modify_txt(filelist)
	hebing_txt(filelist)
	# delete_new_file(filelist)

if __name__=="__main__":
	main()



