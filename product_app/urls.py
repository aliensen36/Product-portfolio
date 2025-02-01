from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.conf import settings
from django.conf.urls.static import static

# Создаем роутер и регистрируем вьюсеты
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]