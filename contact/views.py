from rest_framework import generics, permissions
from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactMessageListCreateView(generics.ListCreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    filterset_fields = ('is_read',)
    search_fields = ('name', 'email', 'message')
    ordering_fields = ('created_at',)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAdminUser()]
        elif self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class ContactMessageRetrieveView(generics.RetrieveAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = (permissions.IsAdminUser,)
