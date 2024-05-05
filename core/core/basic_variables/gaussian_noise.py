import math
from constants import GREY_LEVEL


class Gaussian_Noise:
	"""Гауссовский шум — статистический шум, имеющий плотность вероятности,
	равную плотности вероятности нормального распределения,
	также известного как гауссовское[1][2].
	Другими словами, значения, которые может принимать такой шум,
	имеют гауссовское распределение.
	Принимает:
	mean - среднее значение (integer || float),
	standard_deviation - стандартное отклонение (integer || float)
	"""
	def __init__(
				self,
				mean: float,
				standard_deviation: float) -> None:
		self.mean = mean
		self.standard_deviation = standard_deviation
		self.z = GREY_LEVEL

	def __grey_level(self):
		return ((self.z-self.mean) ** 2) / (2 * self.standard_deviation ** 2)

	@property
	def gaussian_noise(self):
		left = 1 / (self.standard_deviation * math.sqrt(2 * math.pi))
		return left * (math.e ** (-self.__grey_level()))


# Test
if __name__ == '__main__':
	GN = Gaussian_Noise(mean=49.8, standard_deviation=14.77980040460628)
	print(GN.gaussian_noise)
