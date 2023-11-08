from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class Card(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     cardId=models.IntegerField()
#     AccountNum=models.CharField(max_length=100)
    
class institution():
    institutionID= models.AutoField(primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    access_token=models.CharField(max_length=255)