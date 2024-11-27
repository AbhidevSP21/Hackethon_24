from django.db import models

# Create your models here.
class FashionItem(models.Model):
    article_type = models.CharField(max_length=100)
    base_colour = models.CharField(max_length=100)
    season = models.CharField(max_length=50)
    product_display_name = models.CharField(max_length=200)


    def __str__(self):
        return self.product_display_name
