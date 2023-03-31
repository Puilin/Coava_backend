from django.db import models

# Create your models here.
class User(models.Model): # user table
    nickname = models.CharField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    is_activated = models.BooleanField(default=False)
    email = models.CharField(max_length=255, null=False, unique=True)
    phone = models.CharField(max_length=14, null=True)
    country = models.CharField(max_length=255, null=True)
    token = models.PositiveIntegerField(default=0)
    intro = models.CharField(max_length=255, null=True)

class Daily(models.Model): #출석체크
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.JSONField()

class Meme(models.Model): #밈
    title = models.CharField(max_length=255, null=False)
    detail = models.CharField(max_length=255, null=False)
    image = models.CharField(max_length=255, null=False)

class Buzz(models.Model): #출석체크
    title = models.CharField(max_length=255, null=False)
    detail = models.CharField(max_length=255, null=False)
    image = models.CharField(max_length=255, null=False)