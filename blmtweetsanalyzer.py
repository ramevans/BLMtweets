from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from tweepy import Stream

import numpy as np
import pandas as pd


class TwitterClient():
    #twitter Client
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenicate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
            return tweets

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

class TwitterAuthenticator():
    #Twitter credentials
    def authenicate_twitter_app(self):
        auth = OAuthHandler("xxxxxxxxxxx,xxxxxxxxx")
        auth.set_access_token("xxxxxxxxxxxxx,xxxxxxxxxxxxx")
        return auth

class TwitterStreamer():
#Twitter Streamer
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):

        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenicate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list)
# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


class TweetAnalyzer():
    # Functionality for analyzing and categorizing content from num_tweets
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets],columns=['Tweets'])

        df['date'] = np.array([tweet.created_at for tweet in tweets])

        return df


if __name__ == '__main__':

    hash_tag_list = ["#blm", "#blacklivesmatter", "blacklivesmatter", "black lives matter"]
    fetched_tweets_filename = "tweets.txt"

    twitter_streamer = TwitterStreamer()
    tweets = twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()
    tweet_analyzer = TweetAnalyzer()

    #tweets = api.user_timeline (screen_name="realDonaldTrump", count = 20)

    df = tweet_analyzer.tweets_to_data_frame(tweets)


    print(df.head(10))
