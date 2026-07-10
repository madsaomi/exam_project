from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='staff-dashboard'),

    path('categories/', views.category_list, name='staff-category-list'),
    path('categories/create/', views.category_create, name='staff-category-create'),
    path('categories/<int:pk>/edit/', views.category_update, name='staff-category-update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='staff-category-delete'),

    path('dishes/', views.dish_list, name='staff-dish-list'),
    path('dishes/create/', views.dish_create, name='staff-dish-create'),
    path('dishes/<int:pk>/edit/', views.dish_update, name='staff-dish-update'),
    path('dishes/<int:pk>/delete/', views.dish_delete, name='staff-dish-delete'),

    path('news/', views.news_list, name='staff-news-list'),
    path('news/create/', views.news_create, name='staff-news-create'),
    path('news/<int:pk>/edit/', views.news_update, name='staff-news-update'),
    path('news/<int:pk>/delete/', views.news_delete, name='staff-news-delete'),

    path('messages/', views.contact_list, name='staff-contact-list'),
    path('messages/<int:pk>/', views.contact_detail, name='staff-contact-detail'),

    path('about/', views.about_edit, name='staff-about-edit'),
]
