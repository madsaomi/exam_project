from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'field', 'placeholder': 'Email address'}),
            'phone': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Phone number'}),
            'subject': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'field', 'placeholder': 'Message', 'rows': 5}),
        }
