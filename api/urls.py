from django.urls import path,include
from .views import UserID,UserTweets

urlpatterns = [
    path('user-id/', UserID.as_view()),
    path('user-tweets/', UserTweets.as_view()),
    
]