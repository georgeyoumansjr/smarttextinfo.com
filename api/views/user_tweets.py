from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from get_Tweets_for_user import fetch_user_Tweets_data

class UserTweets(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            
            tweets_count = 10
            try:
                tweets_count = request.data.get('tweets_count')
            except:
                pass
            if tweets_count == None:
                tweets_count = 10

            tweets = fetch_user_Tweets_data(username, tweets_count)
            return Response({'data' :tweets}, status=status.HTTP_200_OK)
        except Exception as e:            
            return Response({'error' : 'Error Occured : ' + e.__str__()}, status = status.HTTP_400_BAD_REQUEST)

