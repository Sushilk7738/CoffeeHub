from django.urls import path
from .api_views import *

urlpatterns = [
    path('coffees/', CoffeeListCreateAPIView.as_view(), name='api-coffee-list'),
    path('coffees/<int:pk>', CoffeeDetailAPIView.as_view(), name='api-coffee-detail'),
    path('cart/add/', AddToCartAPIView.as_view(), name='api-cart-add'),
]