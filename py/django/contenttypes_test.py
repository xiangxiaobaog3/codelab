from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    user = models.Foreign
