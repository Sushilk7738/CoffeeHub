from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.generic import TemplateView ,CreateView, ListView , DetailView, UpdateView, DeleteView
from testapp.models import Coffee
from django.urls import reverse_lazy
# Create your views here.

class HelloView(View):
    def get(self, request):
        return HttpResponse("<h1 align='center'>Welcome to Maid Latte Coffeshop</h1>")

class TempView(TemplateView):
    template_name = 'testapp/hello.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = "Sushil"
        context['company'] = "Accenture" 
        context['salary'] = 1200000
        context['department'] = 'Software Engineer'
        return context
    
class HomeView(View):
    def get(self, request):
        return render(request,'home.html')
    
    
class CoffeeCreateView(CreateView):
    model = Coffee
    fields = "__all__"
    
class CoffeeListView(ListView):
    model = Coffee
    
class CoffeeDetailView(DetailView):
    model = Coffee
    
class CoffeeUpdateView(UpdateView):
    model = Coffee
    fields = ['flavour', 'price', 'image']
    
class CoffeeDeleteView(DeleteView):
    model = Coffee
    success_url = reverse_lazy("cafe")