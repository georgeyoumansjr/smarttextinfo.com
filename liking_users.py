import requests
import os
import json
import pandas as pd
import time
import random
# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
# bearer_token = os.environ.get("BEARER_TOKEN")
bearer_token = os.getenv("BEARER_TOKEN")


def create_url(tweet_id = '1586279455978180608',pagination_token= None):
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    # &pagination_token=7140dibdnow9c7btw482mjwf6zy1tcozjb4fdxmdsq69l
    user_fields = "user.fields=created_at,description,url"
    if pagination_token:
        user_fields +=f'&pagination_token={pagination_token}'


    
    # You can replace the ID given with the Tweet ID you wish to like.
    # You can find an ID by using the Tweet lookup endpoint
    id = tweet_id
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/tweets/{}/liking_users".format(id)
    return url, user_fields


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2LikingUsersPython"
    return r


def connect_to_endpoint(url, user_fields):
    response = requests.request("GET", url, auth=bearer_oauth, params=user_fields)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json() , response.status_code


def main(tweet_id = '1586279455978180608',pagination_token= None):
    # import json
    result_array = []
    try:
        url, tweet_fields = create_url(tweet_id,pagination_token)
        json_response,status_code = connect_to_endpoint(url, tweet_fields)
        result_array.extend(json_response['data'])
        page_token_next = None
        while(json_response['meta']['next_token'] and status_code == 200):
            
            try:
                page_token_next = json_response['meta']['next_token']
                time.sleep(random.randint(5,8))
                url, tweet_fields = create_url(tweet_id = '1586279455978180608',pagination_token= json_response['meta']['next_token'])
                json_response,status_code = connect_to_endpoint(url, tweet_fields)
                print("found data in while loop")
                result_array.extend(json_response['data'])
                # Response : {
                    #     "created_at": "2020-06-25T14:10:09.000Z",
                    #     "description": "",
                    #     "id": "1276155482294620160",
                    #     "name": "Anand",
                    #     "username": "VivekWaghwani"
                    # },
                # print(type(json_response))
            except Exception as e:
                page_token_next = json_response['meta']['next_token']
                print("error in while loop :  ",e )
    except Exception as e:
        print("error : " , e)
        with open('CurrentPageToken.txt' , 'w') as f: 
            f.write(page_token_next)
            f.close()
    # print(type(json.dumps(json_response, indent=4, sort_keys=True)))
    

    created_at_list = []
    description_list = []
    id_list = []
    name_list = []
    username_list = []
    if len(result_array) > 0:
        for obj in result_array:
            created_at_list.append(obj['created_at'])
            description_list.append(obj['description'])
            id_list.append(obj['id'])
            name_list.append(obj['name'])
            username_list.append(obj['username'])

        df = pd.DataFrame({
        'name' : name_list,
        'id' : id_list,
        'username'  : username_list,
        'description' : description_list,
        'created_at' : created_at_list
        })

        df.to_csv(f'{tweet_id}.csv', index=False)
        print("data saved to csv")
    else:
        print('No data found')
    print("process finished !")


if __name__ == "__main__":
    main()