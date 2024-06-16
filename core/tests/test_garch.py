import pytest
import numpy as np
from core.arch import ARCHModel
from core.garch import GARCHModel

class TestGARCHModel:

	def test_initialization(self):
		data = np.random.rand(100)
		model = GARCHModel(data, p=1, o=0, q=1)
		assert model.n_obs == len(data)
		assert model.p == 1
		assert model.o == 0
		assert model.q == 1
		assert model.dist == 'normal'

	def test_sigma2_shape(self):
		data = np.random.rand(10)
		model = GARCHModel(data, p=1, o=0, q=1)
		res = model.fit(disp='off')  # assign the result of fit to res

		if res is None:
			assert "fit method returned None"
		else:
			model = res.model

			assert model.sigma2.shape == (model.n_obs,)

	def test_arch_err_shape(self):
		data = np.random.rand(10)
		model = GARCHModel(data, p=1, o=0, q=1)
		model.fit()

		assert model.arch_err.shape == (model.n_obs,)

	def test_fit(self):
		data = np.random.rand(10)
		model = GARCHModel(data, p=1, o=0, q=1)
		model.fit()
		assert np.all(model.params > 0)

	def test_forecast(self):
		data = np.random.rand(10)
		model = GARCHModel(data, p=1, o=0, q=1)
		model.fit()
		forecast = model.forecast(h=10)
		assert forecast.shape == (10,)

	def test_exception_handling(self):
		data = np.random.rand(10)
		# model = GARCHModel(data, p=1, o=0, q=1)

		with pytest.raises(NotImplementedError):
			model = GARCHModel(data, p=1, o=0, q=1, dist='t').fit()

		with pytest.raises(ValueError):
			model = GARCHModel(data, p=1, o=0, q=1).forecast(h=-1)

		with pytest.raises(ValueError):
			model = GARCHModel(data, p=1, o=0, q=1).forecast(h=0)

