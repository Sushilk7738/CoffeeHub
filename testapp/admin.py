from django.contrib import admin
from .models import Coffee ,CartItem, Contact
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