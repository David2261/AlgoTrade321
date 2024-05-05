import math


class Variance:
	""" Дисперсия.
	В теории вероятностей и статистике условная дисперсия
	- дисперсия случайной величины с учетом значения (значений) одной
	или нескольких других переменных. В частности, в эконометрике условная
	дисперсия также известна как скедастическая функция
	или скедастическая функция.
	Принимает:
	data = набор данных [dict],
	count = количество данных [integer]
	"""
	def __init__(
				self,
				data: dict[int, float],
				count: int):
		self.data = data
		self.count = count

	def __mathematical_expectation(self):
		value = 0
		for i in range(self.count):
			value += self.data[i]
		return value / self.count

	@property
	def mean(self):
		return self.__mathematical_expectation()

	@property
	def variance(self):
		sum_data = 0
		for i in range(self.count):
			sum_data += (self.data[i] - self.__mathematical_expectation()) ** 2
		return sum_data / self.count

	@property
	def standard_deviation(self):
		return math.sqrt(self.variance)


# Test
if __name__ == "__main__":
	data = [45.2, 47, 34.1, 64, 64, 74.3, 31.4, 38.4]
	data_2 = Variance(data=data, count=len(data))
	print(data_2.mean)
	print(data_2.standard_deviation)
