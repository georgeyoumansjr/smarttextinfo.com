from django.shortcuts import render
from django.template import loader
from get_Tweets_for_user import fetch_user_Tweets_data
import ast


def Index(request):
    tweets = None
    errors = None
    users = None
    if request.method == 'POST':
        sort_by = request.POST.get('sort_by')
        tweets_Data = request.POST.get('tweets')
        users_data = request.POST.get('users')
        if sort_by != None and tweets_Data != None:
            tweets_Data = ast.literal_eval(tweets_Data)
            users_data = ast.literal_eval(users_data)
            if sort_by == 'Likes':
                tweets_Data = sorted(tweets_Data, key=lambda x: x['likes'], reverse=True)
            elif sort_by == 'Retweets':
                tweets_Data = sorted(tweets_Data, key=lambda x: x['retweets'], reverse=True)
            tweets = {}
            tweets['users'] = users_data
            tweets['tweets'] = tweets_Data

        else:
            username = request.POST.get('username')
            tweets_count = request.POST.get('tweetsCount')
            if '@' in username:
                username = username.replace('@','')
            if username != None:
                if tweets_count == None or tweets_count == '':
                    tweets_count = 10
                else:
                    tweets_count = int(tweets_count)
                try:
                    tweets = fetch_user_Tweets_data(username, tweets_count)
                except Exception as e:
                    print("Error : ", e.__str__())
                    if e.__str__() == 'data':
                        errors = "Access denied for Twitter API ! "

                    
        
    if tweets != None:
        if len(tweets) < 1:
            errors = "No Tweets available ! "
        else:
            users = tweets['users']
            tweets = tweets['tweets']
            
    context = {
        'tweets': tweets,
        'errors' : errors,
        'users' : users
    }

    return render(request, 'api/hello.html', context)


def DataPage(request):
    tweets = None
    errors = None
    users = None
    if request.method == 'POST':
        sort_by = request.POST.get('sort_by')
        tweets_Data = request.POST.get('tweets')
        users_data = request.POST.get('users')
        if sort_by != None and tweets_Data != None:
            tweets_Data = ast.literal_eval(tweets_Data)
            users_data = ast.literal_eval(users_data)
            if sort_by == 'Likes':
                tweets_Data = sorted(tweets_Data, key=lambda x: x['likes'], reverse=True)
            elif sort_by == 'Retweets':
                tweets_Data = sorted(tweets_Data, key=lambda x: x['retweets'], reverse=True)
            tweets = {}
            tweets['users'] = users_data
            tweets['tweets'] = tweets_Data

        else:
            username = request.POST.get('username')
            tweets_count = request.POST.get('tweetsCount')
            if '@' in username:
                username = username.replace('@','')
            if username != None:
                if tweets_count == None or tweets_count == '':
                    tweets_count = 10
                else:
                    tweets_count = int(tweets_count)
                try:
                    tweets = fetch_user_Tweets_data(username, tweets_count)
                except Exception as e:
                    print("Error : ", e.__str__())
                    if e.__str__() == 'data':
                        errors = "Access denied for Twitter API ! "

                    
        
    if tweets != None:
        if len(tweets) < 1:
            errors = "No Tweets available ! "
        else:
            users = tweets['users']
            tweets = tweets['tweets']
            
    context = {
        'tweets': tweets,
        'errors' : errors,
        'users' : users
    }

    return render(request, 'api/result.html', context)
