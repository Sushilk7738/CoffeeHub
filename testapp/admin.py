from django.contrib import admin
from testapp.models import Coffee ,CartItem
# Register your models here.

class CoffeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'flavour', 'price', 'description']
admin.site.register(Coffee, CoffeeAdmin)

admin.site.register(CartItem)