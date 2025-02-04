from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'partners', PartnerViewSet, basename='partner')
router.register(r'spheres', SphereViewSet, basename='sphere')


urlpatterns = [
    path('', include(router.urls)),
]