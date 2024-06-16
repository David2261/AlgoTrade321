import numpy as np
try:
	from .arch import ARCHModel
except ImportError:
	from arch import ARCHModel


class GARCHModel(ARCHModel):
	def __init__(self, data, p, o, q, dist='normal'):
		super().__init__(data, p, o, q, dist)

	def initialize(self):
		self.arch_err = np.zeros(self.n_obs)
		self.sigma2 = np.zeros(self.n_obs, dtype=np.float64)
		self.sigma2[0] = self.data.var()

	def sigma2_update(self, t):
		if not isinstance(t, (int, float)):
			raise ValueError("epsilon must be a number")
		if np.isnan(t):
			raise ValueError("epsilon cannot be NaN")
		params_slice = self.params[self.p + 1:self.p + 1 + self.q]
		err_slice = self.arch_err[t - np.arange(1, self.q + 1)]
		sigma2_slice = np.clip(
			self.sigma2[t - np.arange(1, self.p + 1)], 1e-10, 1e10)
		self.sigma2[t] = (
			np.sum(params_slice * err_slice ** 2) +
			np.sum(self.params[self.p + 1 + self.q:] * sigma2_slice) +
			self.params[-1][0]
		)

	def fit(self, update_freq=1, disp='off'):
		if disp not in ['off', 'on']:
			raise ValueError("Invalid disp value. Must be 'off' or 'on'.")
		self.initialize()
		self.params = np.random.rand(self.p + 1 + self.q + self.p + 1).reshape(-1, 1)

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
				self.params[self.p + 1 + self.q:] += (
					self.sigma2[t - np.arange(1, self.p + 1)] *
					self.sigma2[t - np.arange(1, self.p + 1)] / self.sigma2[t]
				)
				self.params[-1] += self.sigma2[t] / self.n_obs
			else:
				raise NotImplementedError

	def forecast(self, h):
		if not isinstance(h, int) or h <= 0:
			raise ValueError("h должен быть положительным целочисленным числом!")

		forecast_values = np.zeros(h)
		forecast_values[0] = self.sigma2[-1]

		for t in range(1, h):
			if t <= self.q:
				params_slice = self.params[self.p + 1:self.p + 1 + self.q]
				err_slice = self.arch_err[-np.arange(1, t + 1)].reshape(-1, 1)
				sigma2_slice = self.sigma2[-np.arange(1, t + 1)].reshape(-1, 1)
				forecast_values[t] = (
					np.sum(params_slice * err_slice ** 2, axis=0)[0] +
					np.sum(self.params[self.p + 1 + self.q:] * sigma2_slice, axis=0)[0] +
					self.params[-1][0]
				)
			else:
				params_slice = self.params[self.p + 1:self.p + 1 + self.q]
				forecast_slice = forecast_values[
					t - np.arange(1, self.q + 1)].reshape(-1, 1)
				sigma2_slice = forecast_values[
					t - np.arange(1, self.p + 1)].reshape(-1, 1)
				forecast_values[t] = (
					np.sum(params_slice * np.clip(forecast_slice ** 2, 0, 1e10), axis=0)[0] +
					np.sum(
						self.params[self.p + 1 + self.q:] * np.clip(sigma2_slice, 0, 1e10),
						axis=0)[0] +
					self.params[-1][0]
				)

		return forecast_values


if __name__ == '__main__':
	# данные для модели, работает пока только 17
	data = np.random.normal(size=17)

	model = GARCHModel(data, p=1, o=0, q=1, dist='normal')

	# Оцениваем параметры модели
	model.fit()

	# Прогнозирование дисперсии на 10 шагов вперед
	forecast_values = model.forecast(h=10)

	# Выводим результаты
	print(forecast_values)
