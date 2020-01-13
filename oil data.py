import quandl as q
import pandas as pd
import datetime
from textblob import TextBlob
data = q.get('EIA/PET_RWTC_D')

#convert to percent change instead of absolute value of oil. The value in 2003-03-20 is percent change between 2003-04-17 and 2003-03-20 (4 weeks in the future)
pcChange = data.loc["2003-03-20":"2018-01-26", :].Value.resample("B").bfill().pct_change(periods = 20)
pcChange.index = (pcChange.index.map(lambda date : date + datetime.timedelta(days = -28)))
pcChange = pcChange.loc["2003-03-20":"2017-12-29"]
