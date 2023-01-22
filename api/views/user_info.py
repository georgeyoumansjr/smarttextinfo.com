from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from util import get_user_id
class UserID(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            data = get_user_id(username)
            
            return Response({'data' : data}, status = status.HTTP_200_OK)
        except Exception as e:
            
            return Response({'error' : 'Error Occured : ' + e.__str__()}, status = status.HTTP_400_BAD_REQUEST)

