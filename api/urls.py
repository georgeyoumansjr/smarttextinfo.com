from django.urls import path,include
from .views import UserID,UserTweets,Index

urlpatterns = [
    path('user-id/', UserID.as_view()),
    path('user-tweets/', UserTweets.as_view()),
    # path('test/', Test, name= 'test'),
    path('', Index, name= 'index'),
    
]