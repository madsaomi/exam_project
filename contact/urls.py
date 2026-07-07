from django.urls import path
from .views import ContactMessageListCreateView, ContactMessageRetrieveView

urlpatterns = [
    path('', ContactMessageListCreateView.as_view(), name='contact-list-create'),
    path('<int:pk>/', ContactMessageRetrieveView.as_view(), name='contact-detail'),
]
