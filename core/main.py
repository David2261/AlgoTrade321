""" There is entire point for calculation price by gave data """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import arch



# Generate a random time series with 1000 observations
np.random.seed(123)
ts = np.random.randn(1000)

# Create a pandas dataframe with the time series
df = pd.DataFrame({'returns': ts})

# Create a GARCH model and fit it to the data
model = arch.arch_model(df['returns'], vol='GARCH', p=1, q=1)
results = model.fit()


# Print the model summary
print(results.summary())

# Plot the standardized residuals
# fig = results.plot(annualize='D')
# plt.show()

# Generate statistics and diagnostic plots
print(results.std_resid.describe())
# arch.plot_fit(results)
# plt.show()
