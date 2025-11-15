from django.urls import path
from .api_views import *

urlpatterns = [
    path('coffees/', CoffeeListCreateAPIView.as_view(), name='api-coffee-list'),
    path('coffees/<int:pk>', CoffeeDetailAPIView.as_view(), name='api-coffee-detail'),

    # Cart
    path("cart/", CartAPIView.as_view(), name="api-cart"),
    path('cart/add/', AddToCartAPIView.as_view(), name='api-cart-add'),
    path('cart/count/', CartCountAPIView.as_view(), name= 'cart-count'),
    path("cart/remove/<int:pk>/", RemoveCartItemAPIView.as_view()),

]