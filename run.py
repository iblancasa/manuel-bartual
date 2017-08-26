"""Get the sentiments about the Manuel's thread on Twitter.

Did you read the thread about the Manuel's vacations?
https://twitter.com/ManuelBartual/status/89971948375293542

Get the sentiments of the users in Twitter about the
the story that thrilled Spilberg.
"""
import re
import sys
import os
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob as tb
from textblob.sentiments import NaiveBayesAnalyzer

access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCES_TOKEN_SECRET']
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']


class StdOutListener(StreamListener):
    """Run a Twitter stream to process the sentiments of the tweets."""

    def on_status(self, data):
        """"Callback of tweepy to process each new received tweet."""
        tweet = self.clean(data.text)

        if "RT" not in tweet:
            if data.user.location:
                location = self.clean(data.user.location)
            else:
                location = "None"

            if data.lang:
                lang = data.lang
            else:
                lang = "None"

            blob = tb(tweet, analyzer=NaiveBayesAnalyzer())
            print(str(blob.sentiment.p_pos) + "," +
                  str(blob.sentiment.p_neg) + "," +
                  lang + "," +
                  location)
            sys.stdout.flush()
        return True

    def on_error(self, status):
        """Print the error."""
        print(status)

    @staticmethod
    def clean(text):
        """Remove the strange chars from the text."""
        if text:
            expression = r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"
            return ' '.join(re.sub(expression, " ", text).split())
        return "None"


if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    stream.filter(track=["Manuel Bartual", "Bartual", "@ManuelBartual"])
