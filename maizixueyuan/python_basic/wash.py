class Washer:
	def __init__(self):
		self.water = 0
		self.sour = 0

	def add_water(self, water):
		self.water = water
		print('add water:', self.water)
		

	def add_sour(self, sour):
		self.sour = sour
		print('add sour:', self.sour)

	def start_wash(self):
		print('start wash...')

if __name__ == '__main__':
	w = Washer()
	w.add_water(10)
	w.add_sour(10)
	
