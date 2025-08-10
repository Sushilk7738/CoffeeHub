from django.db import models
from django.urls import reverse
# Create your models here.

class Coffee(models.Model):
    name = models.CharField(max_length=25)
    flavour = models.CharField(max_length=15)
    price = models.FloatField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    description = models.TextField(blank=True , null= True)
    
    def get_absolute_url(self):
        return reverse('cafe')
    
    
class CartItem(models.Model):
    coffee = models.ForeignKey(Coffee , on_delete= models.CASCADE)
    quantity =  models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.coffee.name} x {self.quantity}"
    
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"