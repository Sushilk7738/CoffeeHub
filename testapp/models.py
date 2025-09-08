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
    



STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'), 
]

        
class Order(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    card_number = models.CharField(max_length=16)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    items = models.ManyToManyField(Coffee)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    
    def __str__(self):
        return f"Order by {self.name} - ₹{self.total_price} ({self.status})"
    
    
class Review(models.Model):
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=30)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.coffee.name} ({self.rating})"
        