from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from get_Tweets_for_user import fetch_user_Tweets_data,search_by_hashtag,get_tweets_count_data
import ast
from Trends import get_interest_over_time
from api.tasks import main
from api.models import TweetLikes
from wsgiref.util import FileWrapper
def Index(request):

    return render(request, 'api/index.html')

def UsernameMain(request):
    try:
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

        return render(request, 'api/UsernameMain.html', context)
    except Exception as e:
        print(e)
        return render(request, 'api/UsernameMain.html', context={})


def UsernameResult(request):
    if request.method == 'POST':
        tweets = None
        errors = None
        users = None
        try:
        
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
                        else:
                            errors = 'Unable to get tweets for current username, please check username !'

                            
                
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

            return render(request, 'api/UsernameResult.html', context)
        except Exception as e:
            print(e)
            context = {
                'errors' : e.__str__()

            }
            print("context : ", context)
            return render(request, 'api/UsernameResult.html', context)
    return redirect(to='username')

def TweetLikesScrapeView(request):
    if request.method == 'POST':
        
        try:
        
            tweet_id = request.POST.get('tweet_id')
            
            main.delay(tweet_id)
            print("tweet ID : " , tweet_id)
            context = {'tweet_id' : tweet_id}
            return render(request, 'api/TweetScrapeResult.html', context)
        except Exception as e:
            print(e)
            context = {
                'errors' : e.__str__()

            }
            print("context : ", context)
            return render(request, 'api/UsernameResult.html', context)
    



def HashtagMain(request):
    return render(request, 'api/hashtagMain.html')

def KeywordMain(request): 
    return render(request, 'api/KeywordMain.html')

def TweetCountMain(request): 
    return render(request, 'api/TweetCountMain.html')

def TweetLikersDownloadMain(request): 
    return render(request, 'api/DownloadLikesMain.html')

def TweetLikersDownloadResult(request): 
    
    tweetID = request.POST.get('tweetID')
    tweet_Objs = TweetLikes.objects.filter(tweet_id = tweetID)
    if tweet_Objs.exists():
        selected_tweet_obj = tweet_Objs.order_by("id").last()
        
    
        # Open the file using Django's FileWrapper
        file_wrapper = FileWrapper(selected_tweet_obj.file)
        
        # Build the response
        response = HttpResponse(file_wrapper, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=' + selected_tweet_obj.file.name
        
        return response
    else:
        print("no file found")
        context = {
            'document_not_found': True
        }
        return render(request, 'api/DownloadLikesMain.html', context)


def TweetCountResult(request):
    if request.method == 'GET':
        return redirect(to='tweetCount')
    error = None
    try:
        if request.method == 'POST':
            keyword1 = request.POST.get('keyword1')
            keyword2 = request.POST.get('keyword2')
            result = get_tweets_count_data(keyword1,keyword2)
            keys = []
            for key in result:
                keys.append(key)
            key1_count = sum(item['tweet_count'] for item in result[keys[0]])
            key2_count = sum(item['tweet_count'] for item in result[keys[1]])
            keys_percentage_difference = 0
            if key1_count > key2_count:
                keys_percentage_difference = key1_count/ key2_count
            else:
                keys_percentage_difference = key2_count/ key1_count
            daily_data_1 = {} 
            daily_data_2 = {} 
            unique_keys = []
            if len(result[keys[0]]) < len(result[keys[1]]):
                for data in result[keys[0]]:
                    if data.get('start').split("T")[0] not in unique_keys:
                        unique_keys.append(data.get('start').split("T")[0])
            else:
                for data in result[keys[1]]:
                    if data.get('start').split("T")[0] not in unique_keys:
                        unique_keys.append(data.get('start').split("T")[0])

            for data in result[keys[0]]:
                if (data.get('start').split("T")[0] in unique_keys):
                    if(data.get('start').split("T")[0] in daily_data_1.keys()):
                        daily_data_1[data.get('start').split("T")[0]] += data.get('tweet_count')
                    else:
                        daily_data_1[data.get('start').split("T")[0]] = data.get('tweet_count')
                
            for data in result[keys[1]]:
                if (data.get('start').split("T")[0] in unique_keys):
                    if(data.get('start').split("T")[0] in daily_data_2.keys()):
                        daily_data_2[data.get('start').split("T")[0]] += data.get('tweet_count')
                    else:
                        daily_data_2[data.get('start').split("T")[0]] = data.get('tweet_count')

            daily_data_1_keys= []
            for data in daily_data_1.keys():
                daily_data_1_keys.append(int(data.split('-')[2]))
            daily_data_1_values = []
            daily_data_2_values = []
            for data in daily_data_1.values():
                daily_data_1_values.append(int(data))
            for data in daily_data_2.values():
                daily_data_2_values.append(int(data))
            
            context = {
            'key1' : keys[0],
            'key2' : keys[1],
            'data1' : result[keys[0]],
            'data2' : result[keys[1]],
            'key_1_tweets_count' : key1_count,
            'key_2_tweets_count' : key2_count,
            'keys_percentage_difference' : round(keys_percentage_difference,2),
            'daily_data_1_keys' : (daily_data_1_keys),
            'daily_data_1_values' : (daily_data_1_values),
            'daily_data_2_values' : (daily_data_2_values),

        }
            return render(request, 'api/tweetCountResult.html', context)
    except Exception as e:
        print("Error : " , e)        
        context ={'errors' : f"Please Enter correct keywords and try again !"}
        return render(request, 'api/tweetCountResult.html', context)

def HashtagResult(request):
    if request.method == 'GET':
        return redirect(to='hashtag')
    try:
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
        else:
            errors = f'Unable to find data for # {hashtag}, please try again with a valid hashtag'
        
        context = {
            'tweets': tweets,
            'errors' : errors,
            'users' : users,
            'hashtag' : hashtag
        }

        return render(request, 'api/hashtagResult.html', context)
    except Exception as e:
        print(e)
        context = {
            'errors' : e.__str__(),
            
        }

        return render(request, 'api/hashtagResult.html', context)

def KeywordResult(request):
    if request.method == 'GET':
        return redirect(to='keyword')
    try:
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
        else:
            errors = f"Unable to get data for keyword {keyword}, please try again with a correct keyword !"
        context = {
            'tweets': tweets,
            'errors' : errors,
            'users' : users,
            'keyword' : keyword
        }

        return render(request, 'api/keywordResult.html', context)
    except Exception as e:
        return render(request, 'api/keywordResult.html', context={})

        

def KeywordTrendMain(request): 
    return render(request, 'api/KeywordSearchTrendMain.html')

def KeywordTrendResult(request):
    if request.method == 'GET':
        return redirect(to='keywordTrend')
    try:
        if request.method == 'POST':
            keyword1 = request.POST.get('keyword1')
            x_axis = []
            y_axis = []
            x_axis, y_axis = get_interest_over_time(keyword1)

            #for data in result:
            #    x_axis.append(data['date'])
            #    y_axis.append(int(data['value']))

            context = {'x_axis' : x_axis, 'y_axis' : y_axis, 'keyword' : keyword1}
            return render(request, 'api/KeywordTrendResult.html', context)
    except Exception as e:
        print("Error : ",e)
        context = {'errors' : f'Unable to get search Trends for keyword {keyword1}, please try again with a correct keyword !'}
        return render(request, 'api/KeywordTrendResult.html', context)
    #     result = get_tweets_count_data(keyword1)
    #     keys = []
    #     for key in result:
    #         keys.append(key)
    #     key1_count = sum(item['tweet_count'] for item in result[keys[0]])
    #     key2_count = sum(item['tweet_count'] for item in result[keys[1]])
    #     keys_percentage_difference = 0
    #     if key1_count > key2_count:
    #         keys_percentage_difference = key1_count/ key2_count
    #     else:
    #         keys_percentage_difference = key2_count/ key1_count
    #     daily_data_1 = {} 
    #     daily_data_2 = {} 
    #     unique_keys = []
    #     if len(result[keys[0]]) < len(result[keys[1]]):
    #         for data in result[keys[0]]:
    #             if data.get('start').split("T")[0] not in unique_keys:
    #                 unique_keys.append(data.get('start').split("T")[0])
    #     else:
    #         for data in result[keys[1]]:
    #             if data.get('start').split("T")[0] not in unique_keys:
    #                 unique_keys.append(data.get('start').split("T")[0])

    #     for data in result[keys[0]]:
    #         if (data.get('start').split("T")[0] in unique_keys):
    #             if(data.get('start').split("T")[0] in daily_data_1.keys()):
    #                 daily_data_1[data.get('start').split("T")[0]] += data.get('tweet_count')
    #             else:
    #                 daily_data_1[data.get('start').split("T")[0]] = data.get('tweet_count')
            
    #     for data in result[keys[1]]:
    #         if (data.get('start').split("T")[0] in unique_keys):
    #             if(data.get('start').split("T")[0] in daily_data_2.keys()):
    #                 daily_data_2[data.get('start').split("T")[0]] += data.get('tweet_count')
    #             else:
    #                 daily_data_2[data.get('start').split("T")[0]] = data.get('tweet_count')

    #     daily_data_1_keys= []
    #     for data in daily_data_1.keys():
    #         daily_data_1_keys.append(int(data.split('-')[2]))
    #     daily_data_1_values = []
    #     daily_data_2_values = []
    #     for data in daily_data_1.values():
    #         daily_data_1_values.append(int(data))
    #     for data in daily_data_2.values():
    #         daily_data_2_values.append(int(data))
        
    #     context = {
    #     'key1' : keys[0],
    #     'key2' : keys[1],
    #     'data1' : result[keys[0]],
    #     'data2' : result[keys[1]],
    #     'key_1_tweets_count' : key1_count,
    #     'key_2_tweets_count' : key2_count,
    #     'keys_percentage_difference' : round(keys_percentage_difference,2),
    #     'daily_data_1_keys' : (daily_data_1_keys),
    #     'daily_data_1_values' : (daily_data_1_values),
    #     'daily_data_2_values' : (daily_data_2_values),

    # }
    #     return render(request, 'api/tweetCountResult.html', context)
