import os
import requests
import aiohttp
import requests
import asyncio
from dateutil.parser import parse
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import News

from dotenv import load_dotenv
load_dotenv()

channels_list = [
    '428333',
    '1367531',
    '742143',
    '53037279',
    '25979455',
]


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

def job_func( user_id = None, email=None, end_date=None, User=None ):
    url =f'https://api.twitter.com/2/users/{user_id}/mentions?expansions=attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id&tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type&poll.fields=duration_minutes,end_datetime,id,options,voting_status&media.fields=duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics&max_results=10'
    # &exclude=replies,retweets

    # manipulate time to satisfy stupid twitter api https://api.twitter.com/2/users/44196397/mentions
    now = datetime.now()
    fifteen_minutes_ago = now - timedelta(minutes=15)
    fifteen_minutes_ago = fifteen_minutes_ago.isoformat()[:-3] + 'Z'

    url+= f'&start_time={fifteen_minutes_ago}'

    print('Job Triggered')

    # check if it's the last run




    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response, status = loop.run_until_complete(api_call(url))
    loop.close()

    if now > end_date:
        # decrease job count
        User.active_job_count -= 1
        User.save()
        print(f"Last Trigger: {email}")

    if status != 200:
        for err in response['errors']:
            print(err)
        raise Exception(
            "Request returned an error: {}".format(
                status)
        )

    if response['meta']['result_count'] == 0:
        return print(f"No New Tweets: {email}")

    
    
    return send_email( email, response)

async def api_call(url):
    headers = {'Authorization': f'Bearer {bearer_token}'}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            return await response.json(), response.status



def send_email(email, response):

    text = response['data'][0]['text']
    new_tweet_count = response['meta']['result_count']
    message = f'Your twitter account has {new_tweet_count} new mention(s). \n' + text

    send_mail(
        'New Tweet About You!',
        message,
        'coboaccess@gmail.com',
        [email],
        fail_silently=False,
    )



    print(f'Email Sent to : {email}')
    pass


def get_news():
    
    now = datetime.now()
    fifteen_minutes_ago = now - timedelta(minutes=15)
    fifteen_minutes_ago = fifteen_minutes_ago.isoformat()[:-3] + 'Z'


    for id in channels_list:
        url =f'https://api.twitter.com/2/users/{id}/tweets?expansions=attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id&tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type&poll.fields=duration_minutes,end_datetime,id,options,voting_status&media.fields=duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,non_public_metrics,organic_metrics,promoted_metrics&max_results=100'
        url+= f'&start_time={fifteen_minutes_ago}'
    
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response, status = loop.run_until_complete(api_call(url))
            loop.close()

            if status != 200:
                for err in response['errors']:
                    print(err)
                raise Exception(
                    "Request returned an error: {}".format(
                        status)
                )

            if response['meta']['result_count'] == 0:
                print(f"News Channel {id} : No New Tweets")
                continue

            profile_picture_url = response['includes']['users'][0]['profile_image_url']
            channel_name        = response['includes']['users'][0]['name']

            for data in response['data']:
                created_at = data['created_at']
                created_at = created_at.replace('T', " ")
                created_at = created_at.replace('.000Z', "")
                db_entry = News(
                    tweet = data['text'],
                    likes = data['public_metrics']['like_count'],
                    retweets = data['public_metrics']['retweet_count'],
                    created_at = created_at,
                    channel_name = channel_name,
                    profile_picture_url = profile_picture_url,
                )
                db_entry.save()
                print('News saved to database')
        except Exception as e:
            print(e)
            print(id)

def refill_news():
    print('News Lookup.')
    
    for id in channels_list:
        url =f'https://api.twitter.com/2/users/{id}/tweets?expansions=attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id&tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type&poll.fields=duration_minutes,end_datetime,id,options,voting_status&media.fields=duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,non_public_metrics,organic_metrics,promoted_metrics&max_results=100'
    
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response, status = loop.run_until_complete(api_call(url))
            loop.close()

            if status != 200:
                for err in response['errors']:
                    print(err)
                raise Exception(
                    "Request returned an error: {}".format(
                        status)
                )

            if response['meta']['result_count'] == 0:
                print(f"News Channel {id} : No New Tweets")
                continue

            profile_picture_url = response['includes']['users'][0]['profile_image_url']
            channel_name        = response['includes']['users'][0]['name']

            for data in response['data']:
                created_at = data['created_at']
                created_at = created_at.replace('T', " ")
                created_at = created_at.replace('.000Z', "")
                db_entry = News(
                    tweet = data['text'],
                    likes = data['public_metrics']['like_count'],
                    retweets = data['public_metrics']['retweet_count'],
                    created_at = created_at,
                    channel_name = channel_name,
                    profile_picture_url = profile_picture_url,
                )
                db_entry.save()
            print('News saved to database')
            for i in range(30):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response, status = loop.run_until_complete(api_call(url+'&pagination_token='+response['meta']['next_token']))
                loop.close()

                if status != 200:
                    for err in response['errors']:
                        print(err)
                    raise Exception(
                        "Request returned an error: {}".format(
                            status)
                    )

                if response['meta']['result_count'] == 0:
                    print(f"News Channel {id} : No New Tweets")
                    continue

                profile_picture_url = response['includes']['users'][0]['profile_image_url']
                channel_name        = response['includes']['users'][0]['name']

                for data in response['data']:
                    created_at = data['created_at']
                    created_at = created_at.replace('T', " ")
                    created_at = created_at.replace('.000Z', "")
                    db_entry = News(
                        tweet = data['text'],
                        likes = data['public_metrics']['like_count'],
                        retweets = data['public_metrics']['retweet_count'],
                        created_at = created_at,
                        channel_name = channel_name,
                        profile_picture_url = profile_picture_url,
                    )
                    db_entry.save()
                print('News Saved To Database!')
            
        except Exception as e:
            print(e)
            print(id)