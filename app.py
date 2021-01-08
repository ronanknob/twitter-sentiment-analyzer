import sys
import credentials

from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from tweepy.streaming import StreamListener
from csv import writer
from textblob import TextBlob as tb
from textblob import exceptions as errors
from googletrans import Translator

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
    
    def _classify_sentiment(self, tweet_text):
        try:
            tweet_translated = tb(translator.translate(tweet_text, 'en'))
        except:
            tweet_translated = tb(tweet_text)


        polarity = tweet_translated.sentiment.polarity
        # Sentiments are numbers within the range -1 (negative) to 1 (positive)
        # I've considered 0 (neutral) as positive sentiment.
        if polarity < 0:
            return "negative"
        else:
            return "positive"

    
    def on_status(self, status):
        # In this method, we call sentiment analysis and persist the tweet text and the results on a CSV.
        sentiment = self._classify_sentiment(status.text)
        # I've removed the commas from tweet text to don't crash csv identation
        self._persist_result(status.text.replace(",",""), sentiment)

    def on_error(self, status_code):
        print(status_code)
        return False


# APP FLOW ----------
listener = Listener()
translator = Translator()
stream = Stream(auth=api.auth, listener=listener)
try:
    print('Streaming start. Collecting Portuguese tweets...')
    stream.sample(languages=['pt'])
except KeyboardInterrupt:
    print(" -> Keyboard stop required.")
finally:
    print('-> Disconected from stream.')
    stream.disconnect()