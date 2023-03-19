from django.shortcuts import render, HttpResponse
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from api.utils import * # noqa
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required

User = get_user_model()

# clear the old jobs at start
users = User.objects.all()
for user in users:
    user.active_job_count = 0
    user.save()

scheduler = BackgroundScheduler()
scheduler.start()

@login_required
def ResearchTool(request):

    context = {}

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.user.email
        user = User.objects.get(email=email)
        if user.active_job_count > 2:
            context['errors'] = 'You already have 3 processes running.'
        else:
            if '@' in username:
                username = username.replace('@','')
            if username != None:

                today = datetime.now()
                five_hours_later = today + timedelta(hours=5)
                last_run_date = five_hours_later - timedelta(minutes=15)

                try:
                    user = User.objects.get(email=email)
                    user_id = get_user_id(username)[0]['id']
                    scheduler.add_job( job_func, 'interval', minutes = 15, args=[user_id, email, last_run_date, user], end_date = five_hours_later)
                    print(f'New Job Added : {username} > {email}')
                    user.active_job_count += 1
                    user.save()
                    print(f'{user.email} has {user.active_job_count} job(s)')

                except Exception as e:
                    print("Error : ", e.__str__())
                    if e.__str__() == 'data':
                        errors = "Access denied for Twitter API ! "
                    else:
                        errors = 'Unable to get tweets for current username, please check username !'
                    context['errors']=errors

    return HttpResponse( render(request, 'api/ResearchTool.html', context) )

