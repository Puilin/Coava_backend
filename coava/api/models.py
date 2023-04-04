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

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            Daily.objects.create(userid=self)

class Daily(models.Model): #출석체크
    userid = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    date = models.JSONField(default=list)

class Meme(models.Model): #밈
    title = models.CharField(max_length=255, null=False)
    detail = models.CharField(max_length=255, null=False)
    image = models.CharField(max_length=255, null=False)

class Buzz(models.Model): #출석체크
    title = models.CharField(max_length=255, null=False)
    detail = models.CharField(max_length=255, null=False)
    image = models.CharField(max_length=255, null=False)

class Section(models.Model):
    section_name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.section_name

class Item(models.Model):
    name = models.CharField(max_length=255, null=False)
    section = models.ForeignKey(Section, to_field="section_name", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    date_until = models.DateTimeField(null=True)
    image = models.ImageField(upload_to="media/")