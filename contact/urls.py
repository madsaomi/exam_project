from django.urls import path
from .views import ContactMessageListCreateView

urlpatterns = [
    path('', ContactMessageListCreateView.as_view(), name='contact-list-create'),
]
