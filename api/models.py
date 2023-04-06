from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    token_amount = models.IntegerField(default=25)
    active_job_count = models.IntegerField(default=0)

class News(models.Model):

    channel_name = models.CharField(max_length=50)
    profile_picture_url = models.TextField()
    tweet = models.TextField()
    created_at = models.CharField(max_length=30)
    likes = models.IntegerField(default=0)
    retweets = models.IntegerField(default=0)


