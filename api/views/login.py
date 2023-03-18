from django.shortcuts import render, HttpResponse

def Login(request):
    return HttpResponse( render(request, 'api/login.html',{}))
