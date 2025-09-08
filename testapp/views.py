from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView ,CreateView, ListView , DetailView, UpdateView, DeleteView
from testapp.models import Coffee, CartItem, Order
from django.urls import reverse_lazy
from .forms import ContactForm, CheckoutForm
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
    template_name = 'testapp/coffee_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coffee = getattr(self,'object', None)
        try:
            context['reviews'] = coffee.reviews.all().order_by('-created_at')
        
        except Exception:
            context['reviews'] = []

        return context
    
    
    
    
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
    
class RemoveFromCartView(View):
    def post(self, request, pk):
        cart = request.session.get('cart', {})    

        if str(pk) in cart:
            del cart[str(pk)]
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
        
class About_View(TemplateView):
    template_name = 'testapp/about.html'
    
    
class Contact_View(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'testapp/contact.html', {'form' : form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for showing your love! We're grateful for your message.")
            return redirect('contact')
        return render(request, 'testapp/contact.html', {'form' : form})


# class CheckoutPageView(TemplateView):
#     template_name = 'testapp/checkout.html'


class CheckoutView(View):
    def get(self, request):
        form = CheckoutForm()
        return render(request, 'testapp/checkout.html', {'form': form, 'order': None})

    def post(self, request):
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            cart = request.session.get('cart', {})
            total_price = 0
            items = []

            for pk, item in cart.items():
                total_price += item['price'] * item['quantity']
                coffee = get_object_or_404(Coffee, id=item['coffee_id'])
                items.append(coffee)

            order.total_price = total_price
            order.save()
            order.items.add(*items)

            # cart clear
            request.session['cart'] = {}

        
            return redirect('success')

        
        return render(request, 'testapp/checkout.html', {'form': form, 'order': None})



class OrderListView(ListView):
    model = Order
    template_name = 'testapp/order_list.html'
    context_object_name = 'orders'
    ordering = ['-created_at']


class MarkDeliveryView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk = pk)
        order.status = 'delivered'
        order.save()
        return redirect('order_list')