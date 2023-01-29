from django.shortcuts import render
from django.template import loader
from get_Tweets_for_user import fetch_user_Tweets_data

def Index(request):
    tweets = None
    errors = None
    users = None
    if request.method == 'POST':
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
                
    # context = {
    #     'latest_question_list': [{'id' : 1 , 'name' : 'Tweets'}, {'id' : 2 , 'name' : "Data"}],
    # }
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

# def Test(request):
#     data = request.POST
#     print('data : ' , data)
#     context = {
#         'latest_question_list': [{'id' : 1 , 'name' : 'Book'}, {'id' : 2 , 'name' : "Table"}],
#     }

#     return render(request, 'api/hello.html', context)
    