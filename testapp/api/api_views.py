from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Coffee, CartItem, Order
from rest_framework.permissions import IsAuthenticated
from .serializers import CoffeeSerializer, CartItemSerializer

import razorpay
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

import hmac
import hashlib
from testapp.utils import api_success, api_error


class CoffeeListCreateAPIView(ListCreateAPIView):
    queryset = Coffee.objects.all()
    serializer_class = CoffeeSerializer
    
class CoffeeDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Coffee.objects.all()
    serializer_class = CoffeeSerializer

class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
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
            user = request.user,
            coffee = coffee,
            defaults={'quantity' : 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        cart_count = CartItem.objects.filter(user = request.user).count()
        serializer = CartItemSerializer(cart_item)

        return Response({
            "message" :"Item added to cart!",
            "item" : serializer.data,
            "cart_count":cart_count
        }, status=200)


class CartCountAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        count = CartItem.objects.filter(user=request.user).count()
        return Response({"cart_count" : count})
    
class CartAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        items = CartItem.objects.filter(user = request.user)
        serializer = CartItemSerializer(items, many = True)
        cart_total = sum(item.quantity * item.coffee.price for item in items)
        return Response({"items" : serializer.data, "cart_total" : cart_total})
        
class RemoveCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            item = CartItem.objects.get(id=pk, user=request.user)
            item.delete()
            return Response({"message": "Removed"}, status=200)
        except CartItem.DoesNotExist:
            return Response({"error": "Not found"}, status=404)



    
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

class CreateRazorpayOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("🔥 RECEIVED AMOUNT =", request.data) 
        amount = request.data.get("amount")

        # validate amount
        if not amount:
            return api_error("Amount is required")

        try:
            amount_in_paise = int(float(amount) * 100)
        except ValueError:
            return api_error("Invalid amount")

        # create razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "payment_capture": 1
        })

        # store order in DB
        order = Order.objects.create(
            user=request.user,
            total_price=amount,
            razorpay_order_id=razorpay_order["id"],
            status="pending",
        )

        # response to frontend
        return api_success({
            "key": settings.RAZORPAY_KEY_ID,
            "razorpay_order_id": razorpay_order["id"],
            "order_id": order.id,
            "amount": amount,
            "currency": "INR",
        }, "Razorpay order created")


class VerifyPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_signature = request.data.get("razorpay_signature")
        


        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return api_error("Missing required payment fields")

        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
            hashlib.sha256
        ).hexdigest()

        print("🔍 DEBUG:", razorpay_order_id, razorpay_payment_id, razorpay_signature)
        print("🔍 GENERATED:", generated_signature)

        if generated_signature != razorpay_signature:
            return api_error("Signature Mismatch")

        order_id = request.data.get("order_id")
        try:
            order = Order.objects.get(id = order_id, user = request.user)
        except Order.DoesNotExist:
            return api_error("Order not found")

        order.status = "paid"
        order.razorpay_payment_id = razorpay_payment_id
        order.save()

        cart_items = CartItem.objects.filter(user= request.user)
        
        for item in cart_items:
            order.items.create(
                coffee = item.coffee,
                quantity = item.quantity,
                price = item.coffee.price,
            )

        cart_items.delete()

        return api_success(message="Payment verified successfully!")

