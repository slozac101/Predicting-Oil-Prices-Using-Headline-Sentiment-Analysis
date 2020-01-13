import "oil data.py"
import "sentiment calculation.py"

data = sentiment_df
data.insert(1, "percent_change", pcChange)
training = data.loc["2003-03-20":"2016-12-31",:]
validation = data.loc["2016-12-31":,:]

from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg.fit(training.average_sentiment.to_numpy().reshape(-1, 1), training.percent_change.to_numpy().reshape(-1, 1))

print(reg.intercept_)
print(reg.coef_)

from sklearn import metrics
pc_pred = reg.predict(validation.average_sentiment.to_numpy().reshape(-1, 1))
metrics.mean_absolute_error(pc_pred, validation.percent_change)
