import numpy as np

from core.arch import ARCHModel


def test_arch_model():
    np.random.seed(0)
    n_obs = 100
    data = np.zeros(n_obs)
    data[0] = 0.1
    for t in range(1, n_obs):
        data[t] = 0.5 * data[t-1] + np.random.normal(0, 0.1)

    # Create an instance of the ARCHModel class
    model = ARCHModel(data, p=1, o=0, q=1)

    # Test initialization
    assert model.data.shape == (100,)
    assert model.n_obs == 100
    assert model.p == 1
    assert model.o == 0
    assert model.q == 1
    assert model.dist == 'normal'
    assert model.params is None
    assert model.arch_err is None
    assert model.sigma2 is None

    # Test initialization of model
    model.initialize()
    assert model.arch_err.shape == (100,)
    assert model.sigma2.shape == (100,)

    # Test parameter estimation
    model.fit()
    assert model.params.shape == (4, 1)

    # Test residuals
    model.residuals()
    assert model.arch_err.shape == (100,)

    # Test forecasting
    forecast = model.forecast(h=10)
    assert forecast.shape == (10,)

    print("All tests passed!")
