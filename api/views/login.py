from django.shortcuts import render
from django.contrib.auth.models import User

def Login(request):
        
    return render(request, 'login.html',{})
