from django import forms
from .models import Contact, Order, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        
        fields = ['name', 'email', 'message']

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'address', 'card_number']

        
class ReviewForm(forms.ModelForm):
    class Meta :
        model = Review
        fields = ['name', 'rating', 'comment']
        widgets = {
            'name' : forms.TextInput(attrs={'placeholder' : 'Your name'}),
            'rating': forms.NumberInput(attrs={'min':1 , 'max': 5}),
            'comment': forms.Textarea(attrs={'placeholder': 'Write your review...'}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.help_text = None
            field.widget.attrs.update({
                'class' : 'form-control',
                'placeholder' :field.label
            })