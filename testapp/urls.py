from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('create/', views.CoffeeCreateView.as_view(), name='coffee_create'),
    path('cafe/', views.CoffeeListView.as_view(), name='cafe'),
    path('detail/<int:pk>/', views.CoffeeDetailView.as_view(), name='coffee_detail'),
    path('update/<int:pk>/', views.CoffeeUpdateView.as_view(), name='coffee_update'),
    path('delete/<int:pk>/', views.CoffeeDeleteView.as_view(), name='coffee_delete'),

    # Cart URLs
    path('add-to-cart/<int:pk>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/', views.CartView.as_view(), name='cart'),

    # Informational pages
    path('about/', views.About_View.as_view(), name='about'),
    path('contact/', views.Contact_View.as_view(), name='contact'),

    # Checkout and Orders
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('success/', TemplateView.as_view(template_name="testapp/success.html"), name='success'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/delivered/', views.MarkDeliveryView.as_view(), name='mark_delivered'),

    # Authentication
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]
