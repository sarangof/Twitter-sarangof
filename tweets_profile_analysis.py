import operator 
import json
from collections import Counter
from nltk.corpus import stopwords
import string
import vincent
import pandas as pd
import json
import re
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

punctuation = list(string.punctuation)
stop = stopwords.words('english') + stopwords.words('spanish')+ punctuation + ['rt','RT', 'via']

count_all = []#Counter()
count_stop = []
dates_all = []
dates_LDC = []
fname = 'saras-tweets.json'
"""
with open(fname, 'r') as f:
    tweets = json.loads(f.read())
    count_all = []#Counter()
    for tweet in tweets:
        terms_all = [term for term in preprocess(tweet['text'])] # Create a list with all the terms
        terms_stop = [term for term in preprocess(tweet['text']) if term.lower() not in stop]
        terms_only = [term for term in preprocess(tweet['text']) if term not in stop and not term.startswith(('#', '@'))] 
        terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
        # track when the hashtag is mentioned
        dates_all.append(tweet['created_at'])
        count_all = count_all + terms_all
        count_stop = count_stop + terms_stop
        if '#LunesDeCiudad' in terms_hash:
            dates_LDC.append(tweet['created_at'])

#print(Counter(count_stop).most_common(100))
"""

dates_LDC = []
dates_all = []
# f is the file pointer to the JSON data set
with open(fname, 'r') as f:
    tweets = json.loads(f.read())
    for tweet in tweets:
        # let's focus on hashtags only at the moment
        terms_stop = [term for term in preprocess(tweet['text']) if term.lower() not in stop]
        # track when the hashtag is mentioned
        if '#LunesDeCiudad' in terms_stop:
            dates_LDC.append(tweet['created_at'])

        dates_all.append(tweet['created_at'])
        count_stop = count_stop + terms_stop
 
# a list of "1" to count the hashtags
ones = [1]*len(dates_all)
# the index of the series
idx = pd.DatetimeIndex(dates_all)
# the actual series (at series of 1s for the moment)
all_tweets = pd.Series(ones, index=idx)
 
# Resampling / bucketing
per_minute = all_tweets.resample('1Min', how='sum').fillna(0)

time_chart = vincent.Line(all_tweets)
time_chart.axis_titles(x='Time', y='Freq')
time_chart.to_json('time_chart.json')

word_freq = Counter(count_stop).most_common(20)
labels, freq = zip(*word_freq)
data = {'data': freq, 'x': labels}
bar = vincent.Bar(data, iter_idx='x')
bar.to_json('term_freq.json')

