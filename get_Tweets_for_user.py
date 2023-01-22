import requests
import os
import json
from util import get_user_id
from dotenv import load_dotenv
load_dotenv()
# Getting bearer token from .env file
bearer_token = os.getenv("BEARER_TOKEN")

# This is user id for elon musk twitter account
# user_id = '44196397'
user_id = ''
# The number of tweets we'd like to get in our response
max_results = 0



def bearer_oauth(r):
    """
    Method required by bearer token authentication., this sets bearer token in header
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r

def connect_to_endpoint():
    """
    This function makes the get request to get the tweets, if it doesn't get a 200 status response, it raises an error
    """

    # The url to get tweets from user id, it gets info for every option avaialable, and excludes retweets and replies
    url =f'https://api.twitter.com/2/users/{user_id}/tweets?expansions=attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id&tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type&poll.fields=duration_minutes,end_datetime,id,options,voting_status&media.fields=duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,non_public_metrics,organic_metrics,promoted_metrics&max_results={max_results}&exclude=replies,retweets'


    response = requests.request("GET", url, auth=bearer_oauth,)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def main(username, tweet_count):
    global user_id, max_results
    # Getting user id from username:
    user_id = get_user_id(username)[0]['id']
    max_results = tweet_count
    # Sending the request to the specified url
    json_response = connect_to_endpoint()
    # Naming a file in which we will save the response
    out_file = open("myfileNew.json", "w")
#   putting the response in json file
    json.dump(json_response, out_file, indent = 6)
    out_file.close()
    # Separating data of tweets into a new file
    tweet_data = []
    for data in json_response['data']:
        # Getting tweet language, if present
        language = ''
        try:
            language = data['lang']
        except:
            pass
        # preparing data for tweets file
        tweet_data.append({
            'tweet' : data['text'],
            'likes' : data['public_metrics']['like_count'],
            'retweets' : data['public_metrics']['retweet_count'],
            'reply' : data['public_metrics']['reply_count'],
            'quotes' : data['public_metrics']['quote_count'],
            'impressions' : data['public_metrics']['impression_count'],
            'language' : language

        })
    out_file_2 = open("tweets2.json", "w")
#   putting the response in json file
    json.dump(tweet_data, out_file_2, indent = 6)
    out_file_2.close()
# copying above function to be used separately in Django
def fetch_user_Tweets_data(username, tweet_count):

    
    global user_id, max_results
    # Getting user id from username:
    user_id = get_user_id(username)[0]['id']
    max_results = tweet_count
    # Sending the request to the specified url
    json_response = connect_to_endpoint()
    print("response : ", len(json_response['data']))
    tweet_data = []
    for data in json_response['data']:
        # Getting tweet language, if present
        language = ''
        try:
            language = data['lang']
        except:
            pass
        # preparing data for tweets 
        tweet_data.append({
            'tweet' : data['text'],
            'likes' : data['public_metrics']['like_count'],
            'retweets' : data['public_metrics']['retweet_count'],
            'reply' : data['public_metrics']['reply_count'],
            'quotes' : data['public_metrics']['quote_count'],
            'impressions' : data['public_metrics']['impression_count'],
            'language' : language

        })

    return tweet_data
    
if __name__ == "__main__":
    # Sending username and number of tweets to get
    main('elonmusk', 5)
