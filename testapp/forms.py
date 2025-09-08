from django import forms
from .models import Contact, Order, Review

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        
        fields = ['name', 'email', 'message']

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'address', 'card_number']

        
class ReviewForm(forms.ModelForm):
    class meta :
        model = Review
        fields = ['name', 'rating', 'comment']
        widgets = {
            'name' : forms.TextInput(attrs={'placeholder' : 'Your name'}),
            'rating': forms.NumberInput(attrs={'min':1 , 'max': 5}),
            'comment': forms.Textarea(attrs={'placeholder': 'Write your review..'}),
        }