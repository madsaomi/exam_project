from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, DishViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('dishes', DishViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
