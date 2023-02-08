from django.shortcuts import render
from django.template import loader
from get_Tweets_for_user import fetch_user_Tweets_data,search_by_hashtag
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


def HashtagMain(request):
    return render(request, 'api/hashtagMain.html')

def KeywordMain(request):
    return render(request, 'api/KeywordMain.html')

def HashtagResult(request):
    tweets = None
    errors = None
    users = None
    hashtag = None
    if request.method == 'POST':
        sort_by = request.POST.get('sort_by')
        tweets_Data = request.POST.get('tweets')
        users_data = request.POST.get('users')
        hashtag = request.POST.get('hashtag')
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
            hashtag = request.POST.get('hashtag') 
            tweets_count = request.POST.get('tweetsCount')
            if '#' in hashtag:
                hashtag = hashtag.replace('#','')
            if hashtag != None:
                if tweets_count == None or tweets_count == '':
                    tweets_count = 10
                else:
                    tweets_count = int(tweets_count)
                try:
                    tweets = search_by_hashtag(hashtag, tweets_count)
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
        'users' : users,
        'hashtag' : hashtag
    }

    return render(request, 'api/hashtagResult.html', context)

def KeywordResult(request):
    tweets = None
    errors = None
    users = None
    keyword = None
    if request.method == 'POST':
        sort_by = request.POST.get('sort_by')
        tweets_Data = request.POST.get('tweets')
        users_data = request.POST.get('users')
        keyword = request.POST.get('keyword')
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
            keyword = request.POST.get('keyword') 
            tweets_count = request.POST.get('tweetsCount')
            if '#' in keyword:
                keyword = keyword.replace('#','')
            if keyword != None:
                if tweets_count == None or tweets_count == '':
                    tweets_count = 10
                else:
                    tweets_count = int(tweets_count)
                try:
                    tweets = search_by_hashtag(keyword, tweets_count, is_hashtag = False)
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
        'users' : users,
        'keyword' : keyword
    }

    return render(request, 'api/keywordResult.html', context)
    
