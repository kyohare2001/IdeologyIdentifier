# import python libraries to use HTTP requests
import requests

# create a class method to get facebook data
class FacebookData:
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    def get_user_post(self):
        # collect user posts from facebook API
        pass

    