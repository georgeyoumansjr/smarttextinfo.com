from django.shortcuts import render
from django.template import loader

def Index(request):
    if request.method == 'POST':
        print("data in index  : ", request.POST)
    context = {
        'latest_question_list': [{'id' : 1 , 'name' : 'Tweets'}, {'id' : 2 , 'name' : "Data"}],
    }

    return render(request, 'api/hello.html', context)

def Test(request):
    data = request.POST
    print('data : ' , data)
    context = {
        'latest_question_list': [{'id' : 1 , 'name' : 'Book'}, {'id' : 2 , 'name' : "Table"}],
    }

    return render(request, 'api/hello.html', context)
    