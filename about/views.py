from rest_framework import generics
from accounts.permissions import IsAdminOrReadOnly
from .models import AboutContent
from .serializers import AboutContentSerializer


class AboutContentRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = AboutContent.objects.all()
    serializer_class = AboutContentSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = None

    def get_object(self):
        obj, _ = AboutContent.objects.get_or_create(pk=1)
        return obj
