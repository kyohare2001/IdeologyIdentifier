# collect data from Twitter API
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

# os.environ.get()
# Authenticate to access Twitter API
auth = tweepy.OAuthHandler(os.environ.get("api_key"), os.environ.get("api_key_secret"), os.environ.get("access_token"), os.environ.get("access_token_secret"))
api = tweepy.API(auth)

# Collect user names
user_name = "elonmusk"

# collect user id from user name
user = api.get_user(screen_name=user_name)
user_id = user.id_str

# collect user tweets 
tweets = api.user_timeline(screen_name=user_name, count=2, tweet_mode="extended")

for twt in tweets:
    print(twt.id)
    print(twt.created_at)
    print(twt.full_text)



    


