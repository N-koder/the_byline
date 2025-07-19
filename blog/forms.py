from django import forms
from .models import Subscriber

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'w-full p-2 border border-gray-300 rounded'
            })
        }
