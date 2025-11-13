from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Coffee, CartItem
from .serializers import CoffeeSerializer, CartItemSerializer

class CoffeeListCreateAPIView(ListCreateAPIView):
    queryset = Coffee.objects.all()
    serializer_class = CoffeeSerializer
    
class CoffeeDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Coffee.objects.all()
    serializer_class = CoffeeSerializer

class AddToCartAPIView(APIView):
    def post(self, request):
        # 1.extract data
        coffee_id = request.data.get("coffee_id")
        quantity = request.data.get("quantity", 1)

        # 2. validate coffee exists
        try:
            coffee = Coffee.objects.get(id = coffee_id)
        except Coffee.DoesNotExist:
            return Response({"error" : "Coffee not found"}, status=404)
        # 3. Place the GET_OR_CREATE LOGIC HERE
        cart_item, created = CartItem.objects.get_or_create(
            coffee = coffee,
            defaults={'quantity' : quantity}
        )
        
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = CartItemSerializer(cart_item)

        return Response({
            "message" :"Item added to cart!",
            "item" : serializer.data
        }, status=200)
