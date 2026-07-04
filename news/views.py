from rest_framework import viewsets
from accounts.permissions import IsAdminOrReadOnly
from .models import NewsArticle
from .serializers import NewsArticleSerializer


class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    permission_classes = (IsAdminOrReadOnly,)
