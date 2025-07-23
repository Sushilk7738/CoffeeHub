from django.db import models
from django.urls import reverse
# Create your models here.

class Coffee(models.Model):
    name = models.CharField(max_length=25)
    flavour = models.CharField(max_length=15)
    price = models.FloatField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('cafe')