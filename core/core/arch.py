import numpy as np


class ARCHModel():
	"""
	Модель ARCH (авторегрессивная условно гетероскедастическая модель)
	представляет собой модель дисперсии временного ряда.
	Модели ARCH используются для описания изменяющейся, возможно,
	изменчивой дисперсии. Хотя модель ARCH можно использовать для
	описания постепенного увеличения дисперсии с течением времени,
	чаще всего она используется в ситуациях, когда могут быть короткие
	периоды увеличения дисперсии. (Постепенно увеличивающуюся дисперсию,
	связанную с постепенно увеличивающимся средним уровнем,
	лучше обрабатывать путем преобразования переменной.)
	"""
	def __init__(self, data, p, o, q, dist='normal'):
		# data - входные данные
		self.data = data
		# n_obs - количество наблюдений
		self.n_obs = len(data)
		# p - порядок авторегрессии
		self.p = p
		# o - порядок скользящей средней
		self.o = o
		# q - порядок авторегрессии в квадрате остатков
		self.q = q
		# dist - тип распределения ошибок (например, нормальное)
		self.dist = dist
		# params - оценки параметров модели
		self.params = None
		# arch_err - остатки модели ARCH
		self.arch_err = None
		# sigma2 - дисперсия модели ARCH
		self.sigma2 = None
		# forecast - прогнозы модели ARCH
		# self.forecast = None

	def initialize(self):
		self.arch_err = np.zeros(self.n_obs)
		self.sigma2 = np.zeros(self.n_obs)
		self.sigma2[0] = self.data.var()

	def residuals(self):
		"""Метод для расчета остатков модели ARCH"""
		self.initialize()
		self.arch_err[0] = self.data[0]

		for t in range(1, self.n_obs):
			data_slice = self.data[t - np.arange(1, self.p + 2)]
			params_slice = self.params[:self.p + 1]
			self.arch_err[t] = self.data[t] - np.sum(params_slice * data_slice)

	def sigma2_update(self, t):
		"""Метод для обновления дисперсии модели ARCH,
		t - текущий момент времени"""
		params_slice = self.params[self.p + 1:self.p + 1 + self.q]
		err_slice = self.arch_err[t - np.arange(1, self.q + 1)]
		self.sigma2[t] = np.sum(params_slice * err_slice) + self.params[-1].item()

	def fit(self, update_freq=1, disp='off'):
		"""Метод для оценки параметров модели ARCH,
		update_freq - частота обновления параметров
		disp - флаг для вывода информации о процессе оценки"""
		self.initialize()
		self.params = np.random.rand(self.p + 1 + self.q + 1).reshape(-1, 1)

		for t in range(self.p + 1, self.n_obs):
			if t % update_freq == 0:
				print(f'Iteration {t}')

			self.sigma2_update(t)

			if self.dist == 'normal':
				self.params[0] += (
					self.data[t - 1] * self.arch_err[t - 1] / self.sigma2[t]
				)
				self.params[1:self.p + 1] += (
					self.data[t - np.arange(1, self.p + 1)] *
					self.arch_err[t - np.arange(1, self.p + 1)] / self.sigma2[t]
				)
				self.params[self.p + 1:self.p + 1 + self.q] += (
					self.arch_err[t - np.arange(1, self.q + 1)] *
					self.arch_err[t - np.arange(1, self.q + 1)] / self.sigma2[t]
				)
				self.params[-1] += self.sigma2[t] / self.n_obs
			else:
				raise NotImplementedError

	def forecast(self, h):
		"""Метод для прогнозирования дисперсии модели ARCH,
		h - горизонт прогнозирования"""
		if not isinstance(h, int) or h <= 0:
			raise ValueError("h должен быть положительным целочисленным числом!")

		forecast_values = np.zeros(h)
		forecast_values[0] = self.sigma2[-1]

		for t in range(1, h):
			if t <= self.q:
				params_slice = self.params[self.p + 1:self.p + 1 + self.q]
				err_slice = self.arch_err[-np.arange(1, t + 1)].reshape(-1, 1)
				forecast_values[t] = (
					np.sum(params_slice * err_slice, axis=0)[0] + self.params[-1][0]
				)
			else:
				params_slice = self.params[self.p + 1:self.p + 1 + self.q]
				forecast_slice = forecast_values[
					t - np.arange(1, self.q + 1)].reshape(-1, 1)
				forecast_values[t] = (
					np.sum(params_slice * forecast_slice, axis=0)[0] + self.params[-1][0]
				)

		return forecast_values


if __name__ == '__main__':

	data = np.random.normal(size=100)  # генерируем случайный временной ряд

	model = ARCHModel(data, p=1, o=0, q=1, dist='normal')
	model.fit()
	model.residuals()
	print(model.sigma2)
	forecast_values = model.forecast(h=10)
	print(forecast_values)
