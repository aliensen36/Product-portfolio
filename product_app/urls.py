from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProjectViewSet

# Создаем роутер и регистрируем вьюсеты
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    # Подключаем маршруты роутера
    path('', include(router.urls)),
]
