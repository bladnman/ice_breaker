import os
from datetime import datetime, timezone
import logging
import tweepy

logger = logging.getLogger("twitter")

auth = tweepy.OAuthHandler(
    os.environ.get("TWITTER_API_KEY"),
    os.environ.get("TWITTER_API_SECRET")
)
auth.set_access_token(
    os.environ.get("TWITTER_ACCESS_TOKEN"),
    os.environ.get("TWITTER_ACCESS_SECRET")
)
api = tweepy.API(auth)


def scrape_user_tweets(username: str, num_tweets: int = 5):
    """
    Scrape a Twitter user's original tweets (i.e. not retweets) and return
    them as a list of dictionaries.
    Each dictionary contains the following keys:
        "time_posted" (relative to now)
        "text"
        "url"
    """
    tweets = api.user_timeline(screen_name=username, count=num_tweets)
    tweet_list = []
    for tweet in tweets:
        if "RT @" not in tweet.text and not tweet.text.startswith("@"):
            tweet_list.append(
                {
                    "time_posted": str(
                        datetime.now(timezone.utc) - tweet.created_at
                    ),
                    "text": tweet.text,
                    "url": f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
                }
            )
    return tweet_list
