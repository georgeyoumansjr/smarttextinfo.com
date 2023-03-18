from django.shortcuts import render, HttpResponse
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from api.utils import * # noqa

from django.contrib.auth.decorators import login_required

scheduler = BackgroundScheduler()
scheduler.start()

@login_required
def ResearchTool(request):

    context = {}

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.user.email

        if '@' in username:
            username = username.replace('@','')
        if username != None:

            today = datetime.today()
            five_hours_later = (today + timedelta(hours=5)).isoformat()

            try:

                user_id = get_user_id(username)[0]['id']
                scheduler.add_job( job_func, 'interval', minutes = 15, args=[user_id, email], end_date = five_hours_later)

            except Exception as e:
                print("Error : ", e.__str__())
                if e.__str__() == 'data':
                    errors = "Access denied for Twitter API ! "
                else:
                    errors = 'Unable to get tweets for current username, please check username !'
                context['errors']=errors

    return HttpResponse( render(request, 'api/ResearchTool.html', context) )

