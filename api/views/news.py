from django.shortcuts import render, HttpResponse
from datetime import datetime, timedelta
from get_Tweets_for_user import bearer_token
import requests

channels_and_ids_list = [
    {'name': 'CNN',  'id': '428333'},
    {'name': 'FOX',  'id': '1367531'},
    {'name': 'BBC',  'id': '742143'},
]
channels_dict = {
    'CNN':'428333',
    'FOX':'1367531',
    'BBC':'742143',
}
channels_list = [
    '428333',
    '1367531',
    '742143',
]

def News(request):
    context = {}
    tweet_data = []

    for id in channels_list:
        try:
            response = connect_to_endpoint(id)
        except Exception as e:
            print(e)
            print(id)

        profile_picture_url = response['includes']['users'][0]['profile_image_url']
        channel_name =        response['includes']['users'][0]['name']

        for data in response['data']:
            created_at = data['created_at']
            created_at = created_at.replace('T', " ")
            created_at = created_at.replace('.000Z', "")
            tweet_data.append({
                'tweet' : data['text'],
                'likes' : data['public_metrics']['like_count'],
                'retweets' : data['public_metrics']['retweet_count'],
                'created_at' : created_at,
                'channel_name' : channel_name,
                'profile_picture_url' : profile_picture_url,

            })
    tweet_data = sorted(tweet_data, key=lambda x: datetime.strptime(x['created_at'], '%Y-%m-%d %H:%M:%S'), reverse=True)
    for data in tweet_data:
        print('ind data : ')
        print(data)

    context['data'] = tweet_data


    return HttpResponse( render(request, 'api/News.html', context) )

def bearer_oauth(r):
    """
    Method required by bearer token authentication., this sets bearer token in header
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r

def connect_to_endpoint(user_id = None, max_results=10):
    """
    This function makes the get request to get the tweets, if it doesn't get a 200 status response, it raises an error
    """
    # start_date = '2023-01-01T00:00:00Z'
    # end_date = '2023-01-24T23:59:59Z'
    # The url to get tweets from user id, it gets info for every option avaialable, and excludes retweets and replies
    url =f'https://api.twitter.com/2/users/{user_id}/tweets?expansions=attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id&tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type&poll.fields=duration_minutes,end_datetime,id,options,voting_status&media.fields=duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,non_public_metrics,organic_metrics,promoted_metrics&max_results={max_results}'
    # &exclude=replies,retweets
    

    response = requests.request("GET", url, auth=bearer_oauth,)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

# text, created at, pp, name

# tweets [{ channel, text, etc. }]

