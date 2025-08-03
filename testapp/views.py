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
    def post(self,request, pk):
        print("Add to cart view hit ✅") 
        coffee = get_object_or_404(Coffee, id=pk)
        cart = request.session.get('cart' ,  {})

        item_id = str(pk)
    
        if item_id in cart:
            cart[item_id]['quantity'] +=1
        else:
            cart[item_id] = {
                'coffee_id' : coffee.id,
                'name' : coffee.name,
                'price' : float(coffee.price),
                'quantity': 1
            }
        
        request.session['cart'] = cart
        
        return redirect('cart')
    

class CartView(View):
    def get(self, request):
        cart = request.session.get('cart' , {})
        cart_items = []
        total_price = 0

        for pk, item in cart.items():
            try:
                coffee = get_object_or_404(Coffee, id= item['coffee_id'])
                subtotal = item['price'] * item['quantity']
                total_price += subtotal
                
                cart_items.append({
                    'coffee' : coffee,
                    'quantity': item['quantity'],
                    'price': item['price'],
                    'subtotal': subtotal,
                })
                
            except Coffee.DoesNotExist:
                continue
        
        return render(request, 'testapp/cart.html', {
            'cart_items' :cart_items,
            'total_price' : total_price, 
        })