from __future__ import absolute_import, unicode_literals
import os
from django.core.files import File
from django.core.files.storage import default_storage
from celery import shared_task
from datetime import datetime
import time
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'TwitterDjango.settings')

import django
django.setup()
from api.models import TweetLikes

file_path = os.path.join('media' , 'TestingCSV.csv')
# file_path = os.path.join('media' , 'documents' , 'tweets', 'TestingCSV.csv')
tweet_id = '788691542110099'
# with open(file_path, 'rb') as f:
#             tweets = TweetLikes()
#             tweets.tweet_id = tweet_id
#             tweets.file.save(file_path, File(f))
#             tweets.save()



with default_storage.open(file_path, 'rb') as file:
    file_field = File(file)
    tweets = TweetLikes()
    tweets.tweet_id = tweet_id
    tweets.file.save('TestingCSV.csv', file_field)
    tweets.save()