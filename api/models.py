from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    token_amount = models.IntegerField(default=25)
    active_job_count = models.IntegerField(default=0)
