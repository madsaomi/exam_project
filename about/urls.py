from django.urls import path
from .views import AboutContentRetrieveUpdateView

urlpatterns = [
    path('', AboutContentRetrieveUpdateView.as_view(), name='about-detail'),
]
