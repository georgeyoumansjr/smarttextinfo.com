from django.shortcuts import render, redirect
from OpenAI import run
import pycountry
from django.contrib.auth.decorators import login_required

@login_required
def TweetSuggestionView(request): 
    return render(request, 'api/OpenAIMain.html')

@login_required
def TweetSuggestionResultView(request): 
    if request.method == 'POST':
        try:
            if request.user.token_amount < 5:
                context = {'errors' : 'You ran out of quota.'}
                return render(request, 'api/OpenAIResult.html', context)
            print(f'{request.user.email} has {request.user.token_amount} tokens.')
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