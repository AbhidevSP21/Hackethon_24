from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Customers(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)