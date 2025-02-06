from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'partners', PartnerViewSet, basename='partner')
router.register(r'spheres', SphereViewSet, basename='sphere')
router.register(r'product-statuses', ProductStatusViewSet, basename='product-status')
router.register(r'project-statuses', ProjectStatusViewSet, basename='project-status')
router.register(r'sales-models', SalesModelViewSet, basename='sales-model')
router.register(r'project-stages', ProjectStageViewSet, basename='project-stages')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'project-roles', ProjectRoleViewSet, basename='project-role')


urlpatterns = [
    path('', include(router.urls)),
]