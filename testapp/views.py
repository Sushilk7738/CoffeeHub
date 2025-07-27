from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.generic import TemplateView ,CreateView, ListView , DetailView, UpdateView, DeleteView
from testapp.models import Coffee
from django.urls import reverse_lazy
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
    fields = ['flavour', 'price', 'image']
    
class CoffeeDeleteView(DeleteView):
    model = Coffee
    success_url = reverse_lazy("cafe")