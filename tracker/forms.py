from django import forms
from .models import Subscription

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'category', 'amount', 'renewal_date']
        widgets = {
            'renewal_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Netflix'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Entertainment'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }