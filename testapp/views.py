from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.generic import TemplateView ,CreateView, ListView , DetailView, UpdateView, DeleteView
from testapp.models import Coffee, CartItem
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404

# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request,'testapp/home.html')
    
    
class CoffeeCreateView(CreateView):
    model = Coffee
    fields = "__all__"
    
class CoffeeListView(ListView):
    model = Coffee
    template_name = 'testapp/coffee_list.html'
    context_object_name = 'coffee_list'
    
class CoffeeDetailView(DetailView):
    model = Coffee
    context_object_name = 'coffee'
class CoffeeUpdateView(UpdateView):
    model = Coffee
    fields = ['flavour', 'price', 'image', 'description']
    
class CoffeeDeleteView(DeleteView):
    model = Coffee
    success_url = reverse_lazy("cafe")
    
class AddToCartView(View):
    def post(self, request, coffee_id):
        coffee = get_object_or_404(Coffee, id= coffee_id)
        cart_item , created = CartItem.objects.get_or_create(coffee=coffee)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('coffee_list')