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

# Dates during which we'll search for tweets
start_date = None
end_date = None

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
    # start_date = '2023-01-01T00:00:00Z'
    # end_date = '2023-01-24T23:59:59Z'
    # The url to get tweets from user id, it gets info for every option avaialable, and excludes retweets and replies
    url =f'https://api.twitter.com/2/users/{user_id}/tweets?expansions=attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id&tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type&poll.fields=duration_minutes,end_datetime,id,options,voting_status&media.fields=duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,non_public_metrics,organic_metrics,promoted_metrics&max_results={max_results}'
    # &exclude=replies,retweets
    
    if start_date != None and end_date != None:
       url+= f'&start_time={start_date}&end_time={end_date}' 


    response = requests.request("GET", url, auth=bearer_oauth,)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def connect_to_endpoint_for_search_endpoint(hashtag, tweets_count=10):
    """
    This function makes the get request to get the tweets based on query params provided
    """
    try:
        if tweets_count == None or tweets_count == '':
            tweets_count = 10

        url =f'https://api.twitter.com/2/tweets/search/recent?query=%23{hashtag}&expansions=attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id&tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type&poll.fields=duration_minutes,end_datetime,id,options,voting_status&media.fields=duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,non_public_metrics,organic_metrics,promoted_metrics&max_results={tweets_count}'
        
        # if start_date != None and end_date != None:
        #    url+= f'&start_time={start_date}&end_time={end_date}' 


        response = requests.request("GET", url, auth=bearer_oauth,)

        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()
    except Exception as e:
        print("Error : " , e)

def main(username, tweet_count):
    global user_id, max_results
    # Getting user id from username:
    user_id = get_user_id(username)[0]['id']
    max_results = tweet_count
    # Sending the request to the specified url
    json_response = connect_to_endpoint()
    # Naming a file in which we will save the response
    out_file = open("myfileNew2023.json", "w")
#   putting the response in json file
    json.dump(json_response, out_file, indent = 6)
    out_file.close()
    # Separating data of tweets into a new file
    tweet_data = {}
    tweet_data['tweets'] = []
    tweet_data['users'] = []
    
    for data in json_response['data']:
        # Getting tweet language, if present
        language = ''
        try:
            language = data['lang']
        except:
            pass
        # preparing data for tweets file
        tweet_data['tweets'].append({
            'tweet' : data['text'],
            'likes' : data['public_metrics']['like_count'],
            'retweets' : data['public_metrics']['retweet_count'],
            'reply' : data['public_metrics']['reply_count'],
            'quotes' : data['public_metrics']['quote_count'],
            'impressions' : data['public_metrics']['impression_count'],
            'language' : language

        })
    try:
        for data in json_response['includes']['users']:
            tweet_data['users'].append({
                'created_at' : data['created_at'],
                'followers' : data['public_metrics']['followers_count'],
                'following' : data['public_metrics']['following_count'],
                'tweets' : data['public_metrics']['tweet_count'],
                'listed' : data['public_metrics']['listed_count'],
                'profile_Picture' : data['profile_image_url'],
                'name' : data['name'],
                'username' : data['username'],        
            })
    except:
        pass
    out_file_2 = open("tweets22023.json", "w")
#   putting the response in json file
    json.dump(tweet_data, out_file_2, indent = 6)
    out_file_2.close()

def search_by_hashtag(hashtag, tweets_count):
    
    # Sending the request to the specified url
    json_response = connect_to_endpoint_for_search_endpoint(hashtag, tweets_count)
    
    tweet_data = {}
    tweet_data['tweets'] = []
    tweet_data['users'] = []
    for data in json_response['data']:
        # Getting tweet language, if present
        language = ''
        hashtags = ''
        try:
            language = data['lang']
        except:
            pass
        try:
            hashtags_arr = data['entities']['hashtags']
            for hash in hashtags_arr:
                hashtags += hash['tag']
                hashtags += ' , '

        except:
            pass
        media_List = []
        try:
            media_arr = data['attachments']
            for media in media_arr['media_keys']:
                media_List.append(media)
        except:
            pass
        media_data = []
        
        for media_id in media_List:
        
            try:

                matching_dict = [d for d in json_response['includes']['media'] if d['media_key'] == media_id][0]
                media_data.append({
                    'url' : matching_dict['url'],
                    'type' : matching_dict['type'],

                })
            except Exception as e:
                pass
        created_at = None
        try:
            created_at = data['created_at']
            created_at = created_at.replace('T', " ")
            created_at = created_at.replace('.000Z', "")
        except:
            pass
        # preparing data for tweets file
        tweet_data['tweets'].append({
            'tweet' : data['text'],
            'created_at' : created_at,
            'likes' : data['public_metrics']['like_count'],
            'retweets' : data['public_metrics']['retweet_count'],
            'reply' : data['public_metrics']['reply_count'],
            'quotes' : data['public_metrics']['quote_count'],
            'impressions' : data['public_metrics']['impression_count'],
            'language' : language,
            'media' : media_data,
            'hashtags' : hashtags

        })
    try:
        for data in json_response['includes']['users']:
            created_at = None
            try:
                created_at = data['created_at']
                created_at = created_at.replace('T', " ")
                created_at = created_at.replace('.000Z', "")
            except:
                pass
            tweet_data['users'].append({
                'created_at' : created_at,
                'followers' : data['public_metrics']['followers_count'],
                'following' : data['public_metrics']['following_count'],
                'tweets' : data['public_metrics']['tweet_count'],
                'listed' : data['public_metrics']['listed_count'],
                'profile_Picture' : data['profile_image_url'],
                'name' : data['name'],
                'username' : data['username'],        
            })
    except:
        pass
    return tweet_data    

# copying above function to be used separately in Django
def fetch_user_Tweets_data(username, tweet_count, tweet_start_date = None, tweet_end_date = None):

    global user_id, max_results,start_date,end_date
    # Getting user id from username:
    user_id = get_user_id(username)[0]['id']
    max_results = tweet_count

    start_date=tweet_start_date
    end_date=tweet_end_date
    # Sending the request to the specified url
    json_response = connect_to_endpoint()

    tweet_data = {}
    tweet_data['tweets'] = []
    tweet_data['users'] = []
    for data in json_response['data']:
        # Getting tweet language, if present
        language = ''
        hashtags = ''
        try:
            language = data['lang']
        except:
            pass
        try:
            hashtags_arr = data['entities']['hashtags']
            for hash in hashtags_arr:
                hashtags += hash['tag']
                hashtags += ' , '

        except:
            pass
        media_List = []
        try:
            media_arr = data['attachments']
            for media in media_arr['media_keys']:
                media_List.append(media)
        except:
            pass
        media_data = []
        
        for media_id in media_List:
        
            try:

                matching_dict = [d for d in json_response['includes']['media'] if d['media_key'] == media_id][0]
                media_data.append({
                    'url' : matching_dict['url'],
                    'type' : matching_dict['type'],

                })
            except Exception as e:
                pass
        created_at = None
        try:
            created_at = data['created_at']
            created_at = created_at.replace('T', " ")
            created_at = created_at.replace('.000Z', "")
        except:
            pass
        # preparing data for tweets file
        tweet_data['tweets'].append({
            'tweet' : data['text'],
            'created_at' : created_at,
            'likes' : data['public_metrics']['like_count'],
            'retweets' : data['public_metrics']['retweet_count'],
            'reply' : data['public_metrics']['reply_count'],
            'quotes' : data['public_metrics']['quote_count'],
            'impressions' : data['public_metrics']['impression_count'],
            'language' : language,
            'media' : media_data,
            'hashtags' : hashtags

        })
    try:
        for data in json_response['includes']['users']:
            created_at = None
            try:
                created_at = data['created_at']
                created_at = created_at.replace('T', " ")
                created_at = created_at.replace('.000Z', "")
            except:
                pass
            tweet_data['users'].append({
                'created_at' : created_at,
                'followers' : data['public_metrics']['followers_count'],
                'following' : data['public_metrics']['following_count'],
                'tweets' : data['public_metrics']['tweet_count'],
                'listed' : data['public_metrics']['listed_count'],
                'profile_Picture' : data['profile_image_url'],
                'name' : data['name'],
                'username' : data['username'],        
            })
    except:
        pass
    return tweet_data    

if __name__ == "__main__":
    # Sending username and number of tweets to get
    # main('kyliejenner', 20)
    search_by_hashtag('cats')
