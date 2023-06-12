from django.shortcuts import render, HttpResponse
from api.utils import * # noqa
from django.contrib.auth import get_user_model


from django.contrib.auth.decorators import login_required

User = get_user_model()

# clear the old jobs at start
users = User.objects.all()
for user in users:
    user.active_job_count = 0
    user.save()

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from api.utils import get_news
from datetime import datetime, timedelta

# Set up the SQLAlchemy database URL using the SQLite engine

# Create an SQLAlchemy job store using the database URL
jobstore = SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')

scheduler = BackgroundScheduler(jobstores={'default': jobstore})
# scheduler.start()
# # scheduler.remove_all_jobs()
# if not scheduler.get_job('get_news'):
#     scheduler.add_job( get_news, 'interval', id='get_news', minutes = 15, next_run_time=datetime.now()+timedelta(minutes=15))
jobs = scheduler.get_jobs()
print('Jobs :')
for job in jobs:
    print(job)

#print('Clearing duplicates from db')
#from api.models import News
#from django.db.models import Count, Min

#duplicate_objects = News.objects.values('created_at').annotate(Count('id'),id_min=Min('id')).filter(id__count__gt=1)

#for duplicate in duplicate_objects:
#    News.objects.filter(created_at=duplicate['created_at']).exclude(id=duplicate['id_min']).delete()

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

                now = datetime.now()
                five_hours_later = now + timedelta(hours=5)
                last_run_date = five_hours_later - timedelta(minutes=15)

                try:
                    user = User.objects.get(email=email)
                    user_id = get_user_id(username)[0]['id']
                    scheduler.add_job( job_func, 'interval', minutes = 15, next_run_time=now+timedelta(minutes=15), args=[user_id, email, last_run_date, user], end_date = five_hours_later)
                    print(f'New Job Added : {username} > {email}')
                    user.active_job_count += 1
                    user.save()
                    print(f'{user.email} has {user.active_job_count} job(s)')
                    context['success'] = f'Updates about {username} will be sent to {email}'
                except Exception as e:
                    print("Error : ", e.__str__())
                    if e.__str__() == 'data':
                        errors = "Access denied for Twitter API ! "
                    else:
                        errors = 'Unable to get tweets for current username, please check username !'
                    context['errors']=errors

    return HttpResponse( render(request, 'api/ResearchTool.html', context) )

