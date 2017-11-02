#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
from tweepy import OAuthHandler
import json
import io
import unicodedata

consumer_key = '9Mzb5fVyWdUgsScYNEsJIBBCE'
consumer_secret = 'Rm6u2TjsDmN5jZhbe3kJz5iBNq7VHq0Ji7AA7x0Cp0jB51WGZX'

access_token = '43720279-x6cRn0zMGVIV1xHkXfyk2lh39XJKlRxeUTEqlGHE9'
access_secret = '5bIYkaoq0w7ElzMpO6Rzv6uaVTHhaORfyZAcBYmofC8lV'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

with open('saras-tweets.txt', mode='w') as f: #
    json.dump([], f)
n_tweets = []
def process_or_store(tweet):
	with open('saras-tweets.txt', mode='r') as outfile:#, encoding="utf-8"
			feeds = json.load(outfile)
			with open('saras-tweets.txt', mode='w') as outfile2: #, encoding="utf-8"
				tweet['text'] = remove_accents(tweet['text'])
				n_tweets.append(len(feeds))
				if len(feeds)==2:
					print(len(feeds))
				feeds.append(tweet)#unicode(tweet['text']).decode('utf-8'))
				doc = json.dump(feeds, outfile2)#, ensure_ascii=False)

for tweet in tweepy.Cursor(api.user_timeline).items():
	process_or_store(tweet._json)
