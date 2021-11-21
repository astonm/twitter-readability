import os
import re
import sys
import pprint
import tweepy
import readability

clean = re.compile(r"(:?@|http)[^ ]+", re.IGNORECASE)

CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]


def create_client():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    return api


def get_reading_level(api, screen_name, count=200):
    public_tweets = api.user_timeline(
        tweet_mode="extended", count=count, screen_name=screen_name
    )
    all_text = "\n".join(
        [
            clean.sub("", x.full_text)
            for x in public_tweets
            if x.retweeted == False
            and (
                x.in_reply_to_screen_name is None
                or x.in_reply_to_screen_name == x.user.screen_name
            )
        ]
    )

    results = readability.getmeasures(all_text, lang="en")["readability grades"]

    return results


if __name__ == "__main__":
    client = create_client()
    results = get_reading_level(client, sys.argv[1])

    os.system("cls")

    for item in results:
        print(f"{item} : {results[item]}")
