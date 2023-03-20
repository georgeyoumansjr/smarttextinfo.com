from django.shortcuts import render, redirect
from OpenAI import run,runThreads
import pycountry
from django.contrib.auth.decorators import login_required

@login_required
def TweetSuggestionView(request): 
    return render(request, 'api/OpenAIMain.html')

@login_required
def TweetSuggestionResultView(request): 
    if request.method == 'POST':
        try:
            print(f'{request.user.email} has {request.user.token_amount} tokens.')
            if request.user.token_amount < 5:
                context = {'errors' : 'You ran out of free trial quota.'}
                context['quota_error'] = 'Email us at contact@smartdevweb.com about your experience using our app. Our team will review your request and give you additional tokens to use in this tool. You can keep using other features.'
                return render(request, 'api/OpenAIResult.html', context)
            keyword = request.POST.get('keyword')
            emojiOption = request.POST.get('optradio')
            result = run(keyword,emojiOption)
            request.user.token_amount -= 5
            request.user.save()
            context = {'data' : result, 'keyword' : keyword}
            return render(request, 'api/OpenAIResult.html', context)
        except Exception as e:
            print("Error : ", e)
            context = {'errors' : f'Unable to generate tweets for keyword : {keyword}, please try again with a different keyword'}
            return render(request, 'api/OpenAIResult.html', context)
    return redirect(to='AISuggestion')

@login_required
def TweetThreadSuggestionView(request): 
    return render(request, 'api/OpenAIThreadMain.html')


@login_required
def TweetThreadSuggestionResultView(request): 
    if request.method == 'POST':
        try:
            keyword = request.POST.get('keyword')
            emojiOption = request.POST.get('optradio')
            description = request.POST.get('description')
            result = runThreads(keyword,emojiOption, description)
            context = {'data' : result, 'keyword' : keyword}
            return render(request, 'api/OpenAIResult.html', context)
        except Exception as e:
            print("Error : ", e)
            context = {'errors' : f'Unable to generate tweets for keyword : {keyword}, please try again with a different keyword'}
            return render(request, 'api/OpenAIResult.html', context)