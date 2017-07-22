class A:
	def method_p1(self):
		print("p1 method")

	def method_p2(self):
		print("p2 method")

class B(A):
	pass

if __name__ == '__main__':
	a = A()
	a.method_p1()
	a.method_p2()
	b = B()
	b.method_p1()
	b.method_p2()