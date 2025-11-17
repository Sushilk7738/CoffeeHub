
#rest_framework imports
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated

#django imports
from ..models import Coffee, CartItem, OrderItem, Order
from .serializers import CoffeeSerializer, CartItemSerializer
from django.conf import settings
from testapp.utils import api_success, api_error
from django.http import HttpResponse
from django.core.mail import EmailMessage
from io import BytesIO

#razorpay
import razorpay

#hashing
import hmac
import hashlib

#reportlab library imports
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from testapp.utils_email import make_invoice_pdf, send_invoice_mail



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
        print("🔥 CREATE ORDER API HIT BY =", request.user)
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
        order_id = request.data.get("order_id")

        # 1) verify fields
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature, order_id]):
            return api_error("Missing required payment fields")

        # 2) verify signature
        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
            hashlib.sha256
        ).hexdigest()

        if generated_signature != razorpay_signature:
            return api_error("Signature mismatch")

        # 3) fetch order
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return api_error("Order not found")

        # 4) update order
        order.user = request.user
        order.status = "paid"
        order.razorpay_payment_id = razorpay_payment_id
        order.save()

        # 5) Create OrderItem rows correctly
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                coffee=item.coffee,
                quantity=item.quantity,
                price=item.coffee.price
            )

        # 6) clear cart
        cart_items.delete()

        return api_success(message="Payment verified successfully!")


class GenerateInvoiceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return api_error("Order not found")

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="invoice_{order_id}.pdf"'

        pdf = canvas.Canvas(response, pagesize=A4)

        # HEADER
        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawString(140, 780, "MAID LATTE COFFEE SHOP")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(150, 760, "Best Coffee in Mumbai")

        #LOGO
        logo_path = "testapp/static/testapp/images/logo.jpg"
        try:
            pdf.drawImage(logo_path, 40, 740, width=70, height=70, preserveAspectRatio=True)
        except:
            pass  

        pdf.line(40, 720, 550, 720)

        # ORDER DETAILS 
        pdf.setFont("Helvetica", 12)
        pdf.drawString(40, 700, f"Order ID: {order.id}")
        pdf.drawString(40, 680, f"Customer: {order.user.username}")
        pdf.drawString(40, 660, f"Date: {order.created_at.strftime('%d %b %Y, %I:%M %p')}")
        pdf.drawString(40, 640, f"Payment ID: {order.razorpay_payment_id}")

        #ITEMS TABLE HEADER
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, 600, "Item")
        pdf.drawRightString(550, 600, "Amount (Rs.)")
        pdf.line(40, 595, 550, 595)

        pdf.setFont("Helvetica", 12)
        y = 570

        for item in order.items.all():
            item_name = f"{item.coffee.name} (x{item.quantity})"
            amount = f"Rs. {item.price * item.quantity:.2f}"

            pdf.drawString(50, y, item_name)
            pdf.drawRightString(540, y, amount)

            y -= 20

            if y < 100:
                pdf.showPage()
                y = 750

        # TOTAL
        subtotal = sum(item.price * item.quantity for item in order.items.all())

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, y - 20, f"Total Amount (Rs.): {subtotal:.2f}")

        # FOOTER
        pdf.setFont("Helvetica-Oblique", 11)
        pdf.drawCentredString(300, 40, "Thank you for choosing Maid Latte!")

        pdf.save()

        pdf_bytes = make_invoice_pdf(order)
        return response
