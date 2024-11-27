from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Customers(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)

class uploads(models.Model):
   GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
   type_of_cloth = models.CharField(max_length=100)
   color = models.CharField(max_length=50)
   size = models.CharField(max_length=10)
   gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
   upload_file = models.FileField(upload_to='media/')
   userid = models.ForeignKey(Customers, default=1, on_delete=models.CASCADE)

class FashionItem(models.Model):
    article_type = models.CharField(max_length=100)
    base_colour = models.CharField(max_length=100)
    season = models.CharField(max_length=50)
    product_display_name = models.CharField(max_length=200)

