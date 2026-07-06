from rest_framework import viewsets
from accounts.permissions import IsAdminOrReadOnly
from .models import Category, Dish
from .serializers import CategorySerializer, DishSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_fields = ('category', 'is_available')
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'price', 'order')
