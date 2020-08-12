from random import randint

LAST_INDEX = -1

class Ubic(object):
	def __init__(self):
		super(Ubic, self).__init__()
		self._sum = 0
	
	def add(self, part):
		self._sum += part

	def getSum(self):
		return self._sum

class Agr(object):
	def __init__(self, value, ubic):
		super(Agr, self).__init__()
		self._value = value
		self._ubic = ubic

	def value(self):
		return self._value

	def _getPair(self):
		f = randint(1000, 2000)
		s = self.value() - f
		return (f, s) if randint(0,1) else (s, f)

	def process(self, index, part):
		if index == LAST_INDEX:
			return part + self.value()

		f,s = self._getPair()
		self._ubic[0].add(f)
		return part+s


if __name__ == '__main__':
	ubic = [Ubic(),]
	agrs = [Agr(10, ubic), Agr(0, ubic), Agr(21, ubic),]	
	agrs_len = len(agrs)
	part = 0	

	for i, agr in enumerate(agrs):
		if i == agrs_len - 1:
			part = agr.process(LAST_INDEX, part)
		else:
			part = agr.process(i, part)
	print(part, ", ", ubic[0].getSum())