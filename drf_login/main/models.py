from django.db import models
from django.contrib.auth.models import User
# Создайте свои модели здесь.

class userProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    description=models.TextField(blank=True,null=True)
    location=models.CharField(max_length=30,blank=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
class Good(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    price = models.IntegerField()

class Check(models.Model):
    indif = models.CharField(max_length=200,unique=True)
    balance = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Transaction(models.Model):
    indif = models.OneToOneField(Check, null=True, on_delete=models.SET_NULL,)
    history = models.DateTimeField(auto_now=True)
    summ = models.IntegerField()
