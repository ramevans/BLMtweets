from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    listener = StdOutListener()
    #twitter credentials
    auth = OAuthHandler(xxxxxxxxxxx, xxxxxxxxxxxxx)
    auth.set_access_token(xxxxxxxx,xxxxxxxxxxx)

    stream = Stream(auth, listener)

    stream.filter(track=['#blm', '#blacklivesmatter', 'blacklivesmatter', 'black lives matter'])
