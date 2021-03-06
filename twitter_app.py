import tweepy
import sys
import jsonpickle
import os

consumer_key = 'mi1e5x0VX7m7Us5DTD9vovsJR'
consumer_secret = 'wTKhyMG6KRRpvHRns4LExqhvSim3SF7VcVwgohsNZxa2i08MUf'
access_token = '851465774283841537-mbn9MKlb9aqqeEJrqlGzsQaYkdsY3rc'
access_token_secret = '7wIdoEawI1AYk1gjb6xfWQzuZddyGIKZNV5CdzTsFkXI1'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)

#override tweepy.StreamListener to add logic to on_status
# class MyStreamListener(tweepy.StreamListener):

#     def on_status(self, status):
#         print(status.text)

# myStreamListener = MyStreamListener()
# myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())

# myStream.filter(track=['MSFT'])






# searchQuery = ('MSFT', 'en')   # this is what we're searching for
maxTweets = 1# Some arbitrary large number
tweetsPerQry = 1  # this is the max the API permits
fName = 'tweets.txt' # We'll store the tweets in a text file.


# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q='$AAPL', lang='en', count=tweetsPerQry)
                else:
                    new_tweets = api.search(q='$AAPL', lang='en', count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q='$AAPL', lang='en', count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q='$AAPL', lang='en', count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                        '\n')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))


