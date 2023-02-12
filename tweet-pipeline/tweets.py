import tweepy
import pandas as pd
import re
import os
import datetime
from dotenv import load_dotenv
from time import sleep

load_dotenv()


consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def create_df():
    df = pd.DataFrame(columns=[
        'tweet_id', 'tweet_text', 'tweet_created_at', 'tweet_source',
        'tweet_retweet_count', 'tweet_favorite_count', 'user_followers_count',
        'user_created_at','victim_location', 'tweet_url'
    ])
    return df


# max_id -> duplicate almamak icin en son alınan tweet id'sinden sonraki tweetleri alir
def get_tweets(df, hashtags, items=1, max_id=None):
    tweet_dict = {}
    index = 0
    for hashtag in hashtags:
        if max_id:
            cursor = tweepy.Cursor(api.search_tweets, q=hashtag, lang='tr', tweet_mode='extended', max_id=max_id).items(items)
        else:
            cursor = tweepy.Cursor(api.search_tweets, q=hashtag, lang='tr', tweet_mode='extended').items(items)

        try:
            for tweet in cursor:
                # location linki varsa al
                try:
                    victim_location = re.search("(?P<url>https?://[^\s]+)", tweet.full_text).group("url")
                except:
                    victim_location = None

                tweet_url = 'https://twitter.com/twitter/statuses/' + str(tweet.id)

                tweet_dict[index] = {
                    'tweet_id': tweet.id,
                    'tweet_text': tweet.full_text,
                    'tweet_created_at': tweet.created_at,
                    'tweet_source': tweet.source,
                    'tweet_retweet_count': tweet.retweet_count,
                    'tweet_favorite_count': tweet.favorite_count,
                    'user_followers_count': tweet.user.followers_count,
                    'user_created_at': tweet.user.created_at,
                    'victim_location': victim_location,
                    'tweet_url': tweet_url
                }
                index += 1

        except Exception as e:
            print(e)
            pass
        sleep(20)

    df = pd.concat([df, pd.DataFrame.from_dict(tweet_dict, "index")], ignore_index=True)

    return df



if __name__ == '__main__':
    df = create_df()
    hashtags = ['yagma iskenderun -filter:retweets', 'yagma antakya -filter:retweets', 'yagma maras -filter:retweets', 'yagma adana -filter:retweets',
                'yagma adiyaman -filter:retweets', 'yagma deprem -filter:retweets', 'yagma enkaz -filter:retweets', 'yagma yardim -filter:retweets',
                'yagma market -filter:retweets', 'yagma hirsiz -filter:retweets', 'yagma caliyor -filter:retweets', 'yagma antep -filter:retweets']
    df = get_tweets(df, hashtags, items=500, max_id=None)
    df.to_csv(f'./tweet-pipeline/data/tweets_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv', index=False)
