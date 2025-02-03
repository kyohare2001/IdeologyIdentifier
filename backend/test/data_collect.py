# collect data from Twitter API
import tweepy

api_key = "0VjAkpJNF4QvylYL36dRaB3JE"
api_key_secret = "ii4KSHT0b45Ucrnfh23N9TSpNC9Vb4VOdZ37DXiiID3QVFqm7I"
access_token = "1600622828889391104-WLJeYzb1DcoMiwXJJExmTtoo08do1W"
access_token_secret = "CISUsTgcrRV5LquuSohFQKoL0Y2K2f9jJ3371NZ9BSobH"

# Authenticate to access Twitter API
auth = tweepy.OAuthHandler(api_key, api_key_secret, access_token, access_token_secret)
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



    


