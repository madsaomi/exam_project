from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib import messages

from menu.models import Category, Dish
from news.models import NewsArticle
from about.models import AboutContent
from contact.models import ContactMessage
from contact.forms import ContactForm
from accounts.forms import RegisterForm


def home_view(request):
    categories = Category.objects.all()[:8]
    dishes = Dish.objects.filter(is_available=True)[:8]
    news = NewsArticle.objects.filter(is_published=True)[:3]
    return render(request, 'pages/home.html', {
        'categories': categories,
        'dishes': dishes,
        'news': news,
    })


def menu_view(request, cat_id=None):
    categories = Category.objects.all()
    active_category = None
    dishes = Dish.objects.filter(is_available=True)

    if cat_id:
        active_category = get_object_or_404(Category, pk=cat_id)
        dishes = dishes.filter(category=active_category)

    return render(request, 'pages/menu.html', {
        'categories': categories,
        'dishes': dishes,
        'active_category': active_category,
    })


def news_list_view(request):
    news = NewsArticle.objects.filter(is_published=True)
    return render(request, 'pages/news.html', {'news': news})


def news_detail_view(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk, is_published=True)
    return render(request, 'pages/news_detail.html', {'article': article})


def about_view(request):
    about_content = AboutContent.objects.first()
    return render(request, 'pages/about.html', {'about': about_content})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent.')
            return redirect('page-contact')
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('page-home')
    else:
        form = RegisterForm()
    return render(request, 'pages/register.html', {'form': form})
