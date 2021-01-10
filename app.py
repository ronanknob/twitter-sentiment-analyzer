import sys

from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from tweepy.streaming import StreamListener
from csv import writer
from textblob import TextBlob as tb
from textblob import exceptions as errors
from googletrans import Translator

import credentials
import parser
import analyzer

local_file_name = "tweets_output.csv"

# Set tweepy authentication using credentials on credentials.py file. 
auth = OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
auth.set_access_token(credentials.access_token, credentials.access_token_secret)
api = API(auth, wait_on_rate_limit=True,
          wait_on_rate_limit_notify=True)


#override tweepy.StreamListener to add logic to on_status
class Listener(StreamListener):
    def _persist_result(self, tweet_text, sentiment):
        with open(local_file_name, 'a') as csv_file:
            writer_object = writer(csv_file)
            writer_object.writerow([tweet_text, sentiment])
            csv_file.close()
    
    def on_status(self, status):
        # Deal with Retweets. The logic belos prints the full text of the Tweet, or if it’s a Retweet, the full text of the Retweeted Tweet
        # Source http://docs.tweepy.org/en/latest/extended_tweets.html
        if hasattr(status, "retweeted_status"):  # Check if Retweet
            try:
                tweet_text = status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                tweet_text = status.retweeted_status.text
        else:
            try:
                tweet_text = status.extended_tweet["full_text"]
            except AttributeError:
                tweet_text = status.text
        
        # Do some text cleaning in the tweet text
        tweet_treated = parser.parse_tweet(tweet_text)
        # In this method, we call sentiment analysis and persist the tweet text and the results on a CSV.
        sentiment = analyzer.classify_tweet(tweet_treated)
        # I've removed the commas from tweet text to don't crash csv identation
        self._persist_result(tweet_treated.replace(",",""), sentiment)

    def on_error(self, status_code):
        print(status_code)
        return False


# Main flow
listener = Listener()
translator = Translator()
stream = Stream(auth=api.auth, listener=listener)
try:
    print('Streaming start. Collecting Portuguese tweets...')
    stream.sample(languages=['pt'])
except KeyboardInterrupt:
    print(" -> Keyboard stop requested.")
finally:
    print('-> Disconected from stream.')
    stream.disconnect()