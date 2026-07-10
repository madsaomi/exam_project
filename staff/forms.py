from django import forms
from menu.models import Category, Dish
from news.models import NewsArticle
from about.models import AboutContent
from contact.models import ContactMessage


class StaffCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'field'}),
            'description': forms.Textarea(attrs={'class': 'field', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'field'}),
        }


class StaffDishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'field'}),
            'description': forms.Textarea(attrs={'class': 'field', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'field', 'step': '0.01'}),
            'order': forms.NumberInput(attrs={'class': 'field'}),
            'category': forms.Select(attrs={'class': 'field'}),
        }


class StaffNewsForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'field'}),
            'content': forms.Textarea(attrs={'class': 'field', 'rows': 8}),
        }


class StaffAboutForm(forms.ModelForm):
    class Meta:
        model = AboutContent
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'field'}),
            'content': forms.Textarea(attrs={'class': 'field', 'rows': 8}),
        }
