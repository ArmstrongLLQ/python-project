class Turtle:
	def __init__(self, x):
		self.num = x

class Fish:
	def __init__(self, x):
		self.num = x

class Pool:
	def __init__(self, x, y):
		self.turtle = Turtle(x)
		self.fish = Fish(y)

	def print_num(self):
		print('pools have turtle %d, fish %d.' % (self.turtle.num, self.fish.num))

if __name__ == '__main__':
	#turtle = Turtle(4)
	#fish = Fish(3)
	pool = Pool(4, 5)
	pool.print_num()