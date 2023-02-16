from django.urls import path,include
from .views import UserID,UserTweets,Index,DataPage,HashtagMain,HashtagResult,KeywordMain,KeywordResult,TweetCountMain,TweetCountResult

urlpatterns = [
    path('user-id/', UserID.as_view()),
    path('user-tweets/', UserTweets.as_view()),
    # path('test/', Test, name= 'test'),
    path('', Index, name= 'index'),
    path('result/', DataPage, name= 'result'),
    path('hashtag/', HashtagMain, name= 'hashtag'),
    path('hashtag/result/', HashtagResult, name= 'hashtagResult'),
    path('keyword/', KeywordMain, name= 'keyword'),
    path('keyword/result/', KeywordResult, name= 'keywordResult'),
    path('tweetCount/', TweetCountMain, name= 'tweetCount'),
    path('tweetCount/result/', TweetCountResult, name= 'tweetCountResult'),
    
]