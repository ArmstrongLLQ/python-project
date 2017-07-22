import time as t

class MyClock():
	def __init__(self):
		self.unit = ['year', 'month', 'day', 'hour', 'min', 'sec']
		self.prompt = 'not start'
		self.lasted = []
		self.begin = 0
		self.end = 0

	#start timing
	def start(self):
		self.begin = t.localtime()
		print('start')

	def stop(self):
		self.end = t.localtime()
		self._calc()
		print('stop')

	#compute runtime
	def _calc(self):
		self.lasted = []
		self.prompt = 'runtime: '
		for index in range(6):
			self.lasted.append(self.end[index] - self.begin[index])
			if self.lasted[index]:
				self.prompt += str(self.lasted[index]) + self.unit[index]

	def __str__(self):
		return self.prompt

	def __add__(self, other):
		prompt = 'lasted time'
		result = []
		for index in range(6):
			result.append(self.lasted[index] + other.lasted[index])
			if result[index]:
				prompt += str(result[index]) + self.unit[index]
		return prompt

if __name__ == '__main__':
	t1 = MyClock()
	t1.start()
	t.sleep(2)
	t1.stop()
	t2 = MyClock()
	t2.start()
	t.sleep(2)
	t2.stop()
	print('t1 = ' + str(t1))
	print('t2 = ' + str(t2))
	print('t1 + t2 = ' + str(t1 + t2))
	