import pytest
import numpy as np
from core.garch import GARCHModel


class TestGARCHFit:
	def setup_method(self):
		self.data = np.random.normal(size=10)
		self.model = GARCHModel(self.data, p=1, o=0, q=1)

	def test_fit_runs_without_errors(self):
		self.model.fit()

	def test_fit_updates_params(self):
		self.model.initialize()
		self.model.fit()
		initial_params = self.model.params.copy()
		self.model.fit()
		assert not np.array_equal(initial_params, self.model.params)

	def test_fit_updates_sigma2(self):
		self.model.initialize()
		initial_sigma2 = self.model.sigma2.copy()
		self.model.fit()
		assert not np.array_equal(initial_sigma2, self.model.sigma2)

	def test_fit_with_update_freq(self):
		self.model.fit(update_freq=5)
		assert self.model.params.shape == (self.model.p + 1 + self.model.q + self.model.p + 1, 1)

	def test_fit_with_disp(self):
		self.model.fit(disp='on')
		assert self.model.params.shape == (self.model.p + 1 + self.model.q + self.model.p + 1, 1)

	def test_fit_with_invalid_update_freq(self):
		with pytest.raises(ZeroDivisionError):
			self.model.fit(update_freq=0)

	def test_fit_with_invalid_disp(self):
		with pytest.raises(ValueError):
			self.model.fit(disp='invalid')


class TestGARCHSigma2Update:
	def setup_method(self):
		self.data = np.random.rand(10)
		self.model = GARCHModel(self.data, p=1, o=0, q=1)
		self.model.fit(disp='off')

	def test_sigma2_update_invalid_input(self):
		with pytest.raises(ValueError):
			self.model.sigma2_update("invalid")

	def test_sigma2_update_nan_input(self):
		with pytest.raises(ValueError):
			self.model.sigma2_update(np.nan)