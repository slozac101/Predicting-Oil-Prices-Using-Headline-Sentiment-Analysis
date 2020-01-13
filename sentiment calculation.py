import pandas as pd
import datetime
from textblob import TextBlob

def get_headline_sentiment(headline):
    '''
    Utility function to classify sentiment of passed headline
    using textblob's sentiment method
    '''
    # create TextBlob object of passed headline text
    analysis = TextBlob(headline)
    # return sentiment
    return analysis.sentiment.polarity

def get_average_sentiment(oilHeadlines, beginDate, endDate):
    #computes average sentiment of oilHeadlines between two specified dates
    relevantHeadlines = oilHeadlines.loc[oilHeadlines['publish_date'] >= beginDate]
    relevantHeadlines = relevantHeadlines.loc[relevantHeadlines['publish_date'] <= endDate]
    totalPolarity = 0;
    count = 0;
    for headline in relevantHeadlines.headline_text:
        count = count + 1
        totalPolarity = totalPolarity + get_headline_sentiment(headline)
    if count > 0:
        return totalPolarity/count
    else:
        return 0

def get_oil_headlines_sentiments(df):
    #filters by oil headlines and calculates + stores their sentiments in the dataframe
    oilHeadlines = df.loc[df.headline_text.str.contains(r"\boil\b")]
    oilHeadlines.insert(2, "sentiment", oilHeadlines.headline_text.map(lambda headline: get_headline_sentiment(headline)))
    oilHeadlines.publish_date = oilHeadlines.publish_date.map(lambda date : datetime.datetime.strptime(str(date), '%Y%m%d'))
    oilHeadlines = oilHeadlines.loc[oilHeadlines.sentiment != 0]
    return oilHeadlines

def get_monthly_sentiments(oilHeadlines):
    numEntries = 0
    beginDate = datetime.datetime(2003, 2, 20)
    endDate = beginDate + datetime.timedelta(days=28)
    sentimentDictionary = {}
    dates = []
    average_sentiments = []
    while (endDate <= datetime.datetime(2017, 12, 29)):
        if (not (endDate.weekday() == 5 or endDate.weekday() == 6)):
            dates.append(endDate)
            average_sentiments.append(get_average_sentiment(oilHeadlines, beginDate, endDate))
            numEntries += 1
        beginDate += datetime.timedelta(days=1)
        endDate += datetime.timedelta(days=1)
    sentimentDictionary['date'] = dates
    sentimentDictionary['average_sentiment'] = average_sentiments
    return pd.DataFrame.from_dict(sentimentDictionary)

df = pd.read_csv(r"C:\Users\hughd\Documents\MLstocks\abcnews-date-text.csv")
oilHeadlines = get_oil_headlines_sentiments(df)
sentiment_df = get_monthly_sentiments(oilHeadlines)
print(sentiment_df)
