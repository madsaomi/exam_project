from rest_framework import viewsets
from accounts.permissions import IsAdminOrReadOnly
from .models import NewsArticle
from .serializers import NewsArticleSerializer


class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_fields = ('is_published',)
    search_fields = ('title', 'content')
    ordering_fields = ('created_at', 'title')
