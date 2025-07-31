from django.contrib import admin
from testapp.models import Coffee
# Register your models here.

class CoffeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'flavour', 'price', 'description']
admin.site.register(Coffee, CoffeeAdmin)