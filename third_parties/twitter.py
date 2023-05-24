import os
from datetime import datetime, timezone
import logging
import tweepy

logger = logging.getLogger("twitter")


def create_api():
  consumer_key = os.getenv("TWITTER_API_KEY")
  consumer_secret = os.getenv("TWITTER_API_SECRET")
  access_token = os.getenv("TWITTER_ACCESS_TOKEN")
  access_token_secret = os.getenv("TWITTER_ACCESS_SECRET")

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(
    auth, wait_on_rate_limit=True,
  )
  try:
    api.verify_credentials()
  except Exception as e:
    logger.error("Error creating API", exc_info=True)
    raise e
  logger.info("API created")
  return api


def scrape_user_tweets(username: str, num_tweets: int = 5):
  """
  Scrape a Twitter user's original tweets (i.e. not retweets) and return
  them as a list of dictionaries.
  Each dictionary contains the following keys:
      "time_posted" (relative to now)
      "text"
      "url"
  """
  api = create_api()
  print(f"Scraping {username}'s tweets")
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
