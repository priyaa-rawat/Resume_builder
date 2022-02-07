from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    school = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    skills = models.TextField(max_length=1000)
    about_you = models.TextField(max_length=1000)
    previous_work = models.TextField(max_length=1000)
    portfolio = models.URLField()
