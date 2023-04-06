from django.shortcuts import render, HttpResponse
from api.models import News
from .research_tool import scheduler
from api.utils import get_news_with_keyword

def NewsView(request):
    context = {}
    news = News.objects.all().order_by('-created_at')
    context['data'] = news[:100]

    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        if keyword:
            keyword_related_news = news.filter(tweet__icontains=keyword)
            if keyword_related_news:
                try:
                    context['data']    = keyword_related_news[:100]
                except:
                    context['data']    = keyword_related_news
                context['keyword'] = keyword
            else:
                context['errors'] = f'No results found for {keyword}' 

        else:
            context['errors'] = 'Invalid Keyword!'


    return HttpResponse( render(request, 'api/News.html', context) )

def NewsWithKeyworkView(request):
    context = {}
    news = News.objects.all().order_by('-created_at')
    context['data'] = news[:100]

    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        if keyword:
            keyword_related_news = news.filter(tweet__icontains=keyword)
            if keyword_related_news:
                try:
                    context['data']    = keyword_related_news[:100]
                except:
                    context['data']    = keyword_related_news
                context['keyword'] = keyword
            else:
                
                context['errors'] = f'No results found for {keyword}' 

        else:
            context['errors'] = 'Invalid Keyword!'


    return HttpResponse( render(request, 'api/News.html', context) )
