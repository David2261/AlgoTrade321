import pytest
from core.arch import ARCHModel
import numpy as np


def test_init():
	data = np.random.normal(size=100)
	model = ARCHModel(data, p=1, o=0, q=1)
	assert model.data.shape == (100,)
	assert model.p == 1
	assert model.o == 0
	assert model.q == 1
	assert model.dist == 'normal'


def test_initialize():
	data = np.random.rand(100)
	model = ARCHModel(data, p=1, o=0, q=1)
	model.initialize()
	assert model.arch_err.shape == (100,)
	assert model.sigma2.shape == (100,)
	assert model.sigma2[0] == data.var()


def test_residuals():
	data = np.random.normal(size=100)
	model = ARCHModel(data, p=1, o=0, q=1)
	model.params = np.array([0.5, 0.2, 0.1])
	model.residuals()
	assert model.arch_err.shape == (100,)


def test_fit():
	data = np.random.normal(size=100)
	model = ARCHModel(data, p=1, o=0, q=1)
	model.fit()
	assert model.params is not None


def test_arch_model_init():
	data = np.random.rand(100)
	model = ARCHModel(data, p=1, o=0, q=1)
	assert model.data.shape == (100,)
	assert model.n_obs == 100
	assert model.p == 1
	assert model.o == 0
	assert model.q == 1
	assert model.dist == 'normal'
	assert model.params is None
	assert model.arch_err is None
	assert model.sigma2 is None


def test_sigma2_update():
	data = np.random.rand(100)
	model = ARCHModel(data, p=1, o=0, q=1)
	model.params = np.array([0.5, 0.2, 0.1])
	model.initialize()
	model.sigma2_update(10)
	assert model.sigma2[10] == 0.2 * model.arch_err[9]**2 + 0.1


class TestFit:
	def setup_method(self):
		self.data = np.random.normal(size=100)
		self.model = ARCHModel(self.data, p=1, o=0, q=1, dist='normal')

	def test_fit_updates_params(self):
		self.model.fit()
		assert self.model.params is not None
		assert self.model.params.shape == (self.model.p + 1 + self.model.q + 1, 1)

	def test_fit_updates_arch_err(self):
		self.model.fit()
		assert self.model.arch_err is not None
		assert self.model.arch_err.shape == (self.model.n_obs,)

	def test_fit_updates_sigma2(self):
		self.model.fit()
		assert self.model.sigma2 is not None
		assert self.model.sigma2.shape == (self.model.n_obs,)

	def test_fit_with_update_freq(self):
		self.model.fit(update_freq=5)
		assert self.model.params is not None
		assert self.model.params.shape == (self.model.p + 1 + self.model.q + 1, 1)

	def test_fit_with_disp(self):
		self.model.fit(disp='on')
		assert self.model.params is not None
		assert self.model.params.shape == (self.model.p + 1 + self.model.q + 1, 1)

	def test_fit_raises_not_implemented_error(self):
		self.model.dist = 'non_normal'
		with pytest.raises(NotImplementedError):
			self.model.fit()


class TestARCHForecast:
	def setup_method(self):
		self.data = np.random.normal(size=100)
		self.model = ARCHModel(self.data, p=1, o=0, q=1, dist='normal')
		self.model.fit()
		self.model.residuals()

	def test_forecast(self):
		h = 5
		forecast_values = self.model.forecast(h)
		print(forecast_values[0], self.model.sigma2[-1])
		assert forecast_values.shape == (h,)
		assert np.allclose(forecast_values[0], self.model.sigma2[-1])

	def test_forecast_with_small_h(self):
		h = 1
		forecast_values = self.model.forecast(h)
		assert forecast_values.shape == (h,)
		assert np.allclose(forecast_values[0], self.model.sigma2[-1])

	def test_forecast_with_large_h(self):
		h = 20
		forecast_values = self.model.forecast(h)
		assert forecast_values.shape == (h,)
		assert np.allclose(forecast_values[0], self.model.sigma2[-1])

	def test_forecast_with_invalid_h(self):
		h = -1
		with pytest.raises(ValueError):
			self.model.forecast(h)

	def test_forecast_with_non_integer_h(self):
		h = 3.5
		with pytest.raises(ValueError):
			self.model.forecast(h)

	def test_forecast_after_fit(self):
		h = 5
		self.model.fit()
		forecast_values = self.model.forecast(h)
		assert forecast_values.shape == (h,)
		assert np.allclose(forecast_values[0], self.model.sigma2[-1])

	def test_forecast_before_fit(self):
		h = 'dfssdf'
		with pytest.raises(ValueError):
			self.model.forecast(h)
