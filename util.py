import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")

def bearer_oauth(r):
    """
    Method required by bearer token authentication., this sets bearer token in header
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def get_user_id(username):
    url = f'https://api.twitter.com/2/users/by?usernames={username}&user.fields=created_at&expansions=pinned_tweet_id&tweet.fields=author_id,created_at'

    response = requests.request("GET", url, auth=bearer_oauth,)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    data =  response.json()

    return data['data']


