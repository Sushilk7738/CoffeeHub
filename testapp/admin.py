from django.contrib import admin
from .models import Coffee ,CartItem, Contact, Order, Review
# Register your models here.

class CoffeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'flavour', 'price', 'description']
admin.site.register(Coffee, CoffeeAdmin)

admin.site.register(CartItem)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating']
admin.site.register(Review, ReviewAdmin)