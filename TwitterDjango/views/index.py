from django.shortcuts import render
from django.template import loader

def Index(request):
    
    # template = loader.get_template('TwitterDjango/index.html')
    context = {
        'latest_question_list': [{'id' : 1 , 'name' : 'Book'}, {'id' : 2 , 'name' : "Table"}],
    }
    template_path = 'api\\templates\\hello.html'
    return render(request, template_path, context)
    return render(request, 'index.html', context)