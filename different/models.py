from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Bucket_List(models.Model):
    bucket_id = models.CharField(max_length=250 , default='')
    username = models.CharField(max_length=250  , default='')
    item = models.CharField(max_length=350 ,default='')  
    category = models.CharField(max_length=350 , default='')  
    duration = models.CharField(max_length=100 , default='')
    location = models.CharField(max_length=350 , default='')
    status = models.CharField(max_length=250 , default='')

    def __str__(self):
        return f"{self.username} - {self.item}"


class Connect_Users(models.Model):
    username = models.CharField(max_length=250  , default='')
    location = models.CharField(max_length=250 , default='')
    email = models.EmailField(max_length=250 , default='')


    def __str__(self):
        return f"{self.username} - {self.location}"

class Shared_Items(models.Model):
    username = models.CharField(max_length=250  , default='')
    comment = models.CharField(max_length=500 , default='')
    completed_item = models.CharField(max_length=350 ,default='')  

    def __str__(self):
        return f"{self.username} shared {self.completed_item}."
