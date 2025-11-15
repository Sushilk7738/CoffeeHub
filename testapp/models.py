from django.db import models
from django.urls import reverse
from django.conf import settings
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank = True)
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
    



class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Razorpay fields
    razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username if self.user else 'Guest'}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.coffee.name} x {self.quantity}"



    
class Review(models.Model):
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=30)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.coffee.name} ({self.rating})"
        