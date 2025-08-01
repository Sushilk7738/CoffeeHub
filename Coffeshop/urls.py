"""
URL configuration for Coffeshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from testapp import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view()),
    path('home/', views.HomeView.as_view(),name='home'),
    path('create/', views.CoffeeCreateView.as_view()),
    path('cafe/', views.CoffeeListView.as_view(), name='cafe'),
    path('detail/<int:pk>/', views.CoffeeDetailView.as_view()),
    path('update/<int:pk>/', views.CoffeeUpdateView.as_view()),
    path('delete/<int:pk>/', views.CoffeeDeleteView.as_view()),
    path('add-to-cart/<int:pk>/', views.AddToCartView.as_view(), name= 'add_to_cart'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)