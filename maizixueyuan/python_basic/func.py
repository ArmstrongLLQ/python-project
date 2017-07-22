
def func_int(*num_list):
	intput = list(num_list)
	intput.sort()
	return 'min:%s'%intput[0], 'max:%s'%intput[-1]

if __name__ == '__main__':
	intput = input('please input: ')
	num_tuple = (int(n) for n in intput.split())
	print(num_tuple)
	print(func_int(num_tuple))