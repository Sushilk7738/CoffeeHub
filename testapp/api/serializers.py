from rest_framework import serializers
from ..models import Coffee, CartItem

class CoffeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coffee
        fields = ['id', 'name', 'price', 'image', 'flavour']

class CoffeeMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coffee
        fields = ['id', 'name', 'price', 'flavour', 'image']        

class CartItemSerializer(serializers.ModelSerializer):
    coffee = CoffeeMiniSerializer(read_only= True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'coffee', 'quantity', 'total_price', 'added_at']

    def get_total_price(self, obj):
        return obj.quantity * obj.coffee.price

