from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from menu.models import Category, Dish
from news.models import NewsArticle
from contact.models import ContactMessage
from about.models import AboutContent
from .forms import StaffCategoryForm, StaffDishForm, StaffNewsForm, StaffAboutForm


def staff_required(view_func):
    return staff_member_required(login_url='/login/')(view_func)


@staff_member_required(login_url='/login/')
def dashboard(request):
    ctx = {
        'categories': Category.objects.count(),
        'dishes': Dish.objects.count(),
        'news': NewsArticle.objects.count(),
        'messages': ContactMessage.objects.count(),
        'unread': ContactMessage.objects.filter(is_read=False).count(),
    }
    return render(request, 'staff/dashboard.html', ctx)


# === CATEGORIES ===

@staff_member_required(login_url='/login/')
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'staff/category_list.html', {'categories': categories})


@staff_member_required(login_url='/login/')
def category_create(request):
    form = StaffCategoryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Category created')
        return redirect('staff-category-list')
    return render(request, 'staff/category_form.html', {'form': form, 'title_key': 'newCategory'})


@staff_member_required(login_url='/login/')
def category_update(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    form = StaffCategoryForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Category updated')
        return redirect('staff-category-list')
    return render(request, 'staff/category_form.html', {'form': form, 'title_key': 'editCategory'})


@staff_member_required(login_url='/login/')
def category_delete(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Category deleted')
        return redirect('staff-category-list')
    return render(request, 'staff/confirm_delete.html', {'obj': obj, 'title_key': 'deleteCategory'})


# === DISHES ===

@staff_member_required(login_url='/login/')
def dish_list(request):
    dishes = Dish.objects.select_related('category').all()
    return render(request, 'staff/dish_list.html', {'dishes': dishes})


@staff_member_required(login_url='/login/')
def dish_create(request):
    form = StaffDishForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Dish created')
        return redirect('staff-dish-list')
    return render(request, 'staff/dish_form.html', {'form': form, 'title_key': 'newDish'})


@staff_member_required(login_url='/login/')
def dish_update(request, pk):
    obj = get_object_or_404(Dish, pk=pk)
    form = StaffDishForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Dish updated')
        return redirect('staff-dish-list')
    return render(request, 'staff/dish_form.html', {'form': form, 'title_key': 'editDish'})


@staff_member_required(login_url='/login/')
def dish_delete(request, pk):
    obj = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Dish deleted')
        return redirect('staff-dish-list')
    return render(request, 'staff/confirm_delete.html', {'obj': obj, 'title_key': 'deleteDish'})


# === NEWS ===

@staff_member_required(login_url='/login/')
def news_list(request):
    articles = NewsArticle.objects.all()
    return render(request, 'staff/news_list.html', {'articles': articles})


@staff_member_required(login_url='/login/')
def news_create(request):
    form = StaffNewsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'News created')
        return redirect('staff-news-list')
    return render(request, 'staff/news_form.html', {'form': form, 'title_key': 'newNews'})


@staff_member_required(login_url='/login/')
def news_update(request, pk):
    obj = get_object_or_404(NewsArticle, pk=pk)
    form = StaffNewsForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'News updated')
        return redirect('staff-news-list')
    return render(request, 'staff/news_form.html', {'form': form, 'title_key': 'editNews'})


@staff_member_required(login_url='/login/')
def news_delete(request, pk):
    obj = get_object_or_404(NewsArticle, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'News deleted')
        return redirect('staff-news-list')
    return render(request, 'staff/confirm_delete.html', {'obj': obj, 'title_key': 'deleteNews'})


# === CONTACT MESSAGES ===

@staff_member_required(login_url='/login/')
def contact_list(request):
    msgs = ContactMessage.objects.all()
    return render(request, 'staff/contact_list.html', {'msgs': msgs})


@staff_member_required(login_url='/login/')
def contact_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if not msg.is_read:
        msg.is_read = True
        msg.save()
    return render(request, 'staff/contact_detail.html', {'msg': msg})


# === ABOUT ===

@staff_member_required(login_url='/login/')
def about_edit(request):
    obj, _ = AboutContent.objects.get_or_create(pk=1)
    form = StaffAboutForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'About page updated')
        return redirect('staff-dashboard')
    return render(request, 'staff/about_form.html', {'form': form, 'title_key': 'editAboutPage'})
