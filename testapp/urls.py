from django.urls import path
from django.views.generic import TemplateView
from testapp.auth_views import RegisterAPIView, LoginAPIView
from testapp.api.api_views import CreateRazorpayOrderAPIView, VerifyPaymentAPIView, GenerateInvoiceAPIView,CartAPIView
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
    # path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/', TemplateView.as_view(template_name="testapp/checkout.html"), name='checkout'),
    path('success/', TemplateView.as_view(template_name="testapp/success.html"), name='success'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/delivered/', views.MarkDeliveryView.as_view(), name='mark_delivered'),
    path('orders/<int:order_id>/download-invoice/', views.DownloadInvoiceView.as_view(), name='download_invoice'),


    # # Authentication
    # path('signup/', views.SignUpView.as_view(), name='signup'),
    # path('login/', views.UserLoginView.as_view(), name='login'),
    # path('logout/', views.UserLogoutView.as_view(), name='logout'),

    path("api/auth/register/", RegisterAPIView.as_view(), name="jwt-register"),
    path("api/auth/login/", LoginAPIView.as_view(), name="jwt-login"),
    
    # jwtbased login and signup 
    path("login/", TemplateView.as_view(template_name="testapp/login.html"), name="login"),
    path("signup/", TemplateView.as_view(template_name="testapp/signup.html"), name="signup"),

    #order-payment
    path("api/payment/create-order/", CreateRazorpayOrderAPIView.as_view(), name="create_razorpay_order"),
    path("api/payment/verify/", VerifyPaymentAPIView.as_view(), name="verify_payment"),
    path("payment-success/", TemplateView.as_view(template_name="testapp/success.html"), name="payment_success"),

    #invoice 
    path("api/orders/<int:order_id>/invoice/", GenerateInvoiceAPIView.as_view(), name = "order_invoice"),
    path("api/cart/", CartAPIView.as_view(), name="api_cart"),

]
