from django.contrib import admin
from django.urls import path, include, re_path
from django.http import FileResponse
from django.views.static import serve
import os
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from config.settings import BASE_DIR

def portal_view(request):
    f = open(BASE_DIR / 'index.html', 'rb')
    response = FileResponse(f, content_type='text/html; charset=utf-8')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

urlpatterns = [
    path('', portal_view, name='portal'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/menu/', include('menu.urls')),
    path('api/news/', include('news.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/about/', include('about.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    re_path(r'^frontend/(?P<path>.*)$', serve, {'document_root': os.path.join(BASE_DIR, 'frontend')}),
]
