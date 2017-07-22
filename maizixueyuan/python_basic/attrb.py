class TestClass:
	classa = 'classa'
	def __init__(self):
		self.a = 0
		self.b = 0

	def info(self):
		print('a:', self.a, 'b:', self.b)
		print(TestClass.classa)

if __name__ == '__main__':
	t1 = TestClass()
	t1.info()
