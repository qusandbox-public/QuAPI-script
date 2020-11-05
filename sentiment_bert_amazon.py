import requests
import pandas as pd

# helper function on mark the sentence with the sentiment having highest probability
def map_polarity(x):
    if x == 'positive_score':
        return "positive"
    elif x == 'negative_score':
        return 'negative'
    else:
        return "neutral"


sentiment_api_url = "http://test-qs.qusandbox.com/quapi/sentiment/bert/v2/amazon/"
text_list = ['Id now like to turn the call over to Tim for introductory remarks.',
            'Thanks, Tejas. Good afternoon, everyone. Thanks for joining us today. I hope youre staying safe and well.',
            'And that does conclude todays conference. Thank you all for joining us today.']
# generate the request body
body = {'data' : text_list}
# send request to the API
response  = requests.post(sentiment_api_url, json=body)
print(response.json())
# get result from API
sentiments = response.json()['probability']
# process the result of API
df = pd.DataFrame(sentiments, columns = ['positive_score', 'negative_score', 'neutral_score'])
df['text'] = text_list
df.index.names = ['id']
df['sentiment'] = df[['positive_score', 'negative_score', 'neutral_score']].idxmax(axis = 1)
df.sentiment = df.sentiment.map(map_polarity)
print(df)