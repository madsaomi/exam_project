from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from config.page_views import (
    home_view, menu_view, news_list_view, news_detail_view,
    about_view, contact_view, register_view,
)


def healthcheck(request):
    return HttpResponse('ok')


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)


def custom_403(request, exception):
    return render(request, '403.html', status=403)


urlpatterns = [
    path('health/', healthcheck, name='healthcheck'),
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),

    # Staff panel
    path('staff/', include('staff.urls')),

    # Services page — links to admin, staff, API docs
    path('services/', lambda r: render(r, 'pages/services.html'), name='services'),

    # Template pages
    path('pages/', home_view, name='page-home'),
    path('pages/menu/', menu_view, name='page-menu'),
    path('pages/menu/<int:cat_id>/', menu_view, name='page-menu-category'),
    path('pages/news/', news_list_view, name='page-news'),
    path('pages/news/<int:pk>/', news_detail_view, name='page-news-detail'),
    path('pages/about/', about_view, name='page-about'),
    path('pages/contact/', contact_view, name='page-contact'),

    # Auth (session-based)
    path('login/', auth_views.LoginView.as_view(template_name='pages/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),

    # API
    path('api/auth/', include('accounts.urls')),
    path('api/menu/', include('menu.urls')),
    path('api/news/', include('news.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/about/', include('about.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'config.urls.custom_404'
handler500 = 'config.urls.custom_500'
handler403 = 'config.urls.custom_403'
