import tweepy
from tweepy import OAuthHandler
import json

consumer_key = '9Mzb5fVyWdUgsScYNEsJIBBCE'
consumer_secret = 'Rm6u2TjsDmN5jZhbe3kJz5iBNq7VHq0Ji7AA7x0Cp0jB51WGZX'

access_token = '43720279-x6cRn0zMGVIV1xHkXfyk2lh39XJKlRxeUTEqlGHE9'
access_secret = '5bIYkaoq0w7ElzMpO6Rzv6uaVTHhaORfyZAcBYmofC8lV'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

with open('saras-tweets.txt', mode='w') as f: #, encoding='utf-8'
    json.dump([], f)

def process_or_store(tweet):
	with open('saras-tweets.txt', mode='r') as outfile:
			feeds = json.load(outfile)
			with open('saras-tweets.txt', mode='w') as outfile:
				feeds.append(tweet)
				json.dump(feeds, outfile)

for tweet in tweepy.Cursor(api.user_timeline).items():
    process_or_store(tweet._json)