from django.conf import settings
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Product, Project
from .serializers import *

User = settings.AUTH_USER_MODEL  # Получаем модель пользователя через settings.AUTH_USER_MODEL

class ProductViewSet(ModelViewSet):
    """
    Вьюсет для работы с моделью Product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Добавляем возможность фильтрации по статусу через параметр запроса.
        Например: /api/products/?status=active
        """
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    @action(detail=True, methods=['get', 'post'], url_path='owners')
    def owners(self, request, pk=None):
        """
        GET: Возвращает список заказчиков продукта.
        POST: Добавляет заказчика к продукту.
        """
        product = self.get_object()

        if request.method == 'GET':
            owners = product.owners.all()
            data = [{'id': owner.id, 'username': owner.username} for owner in owners]
            return Response(data)

        if request.method == 'POST':
            user_id = request.data.get('user_id')
            if not user_id:
                return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Используем модель пользователя через settings.AUTH_USER_MODEL
                user = User.objects.get(id=user_id)
                product.owners.add(user)
                return Response({'message': f'User {user.username} added as owner.'})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get', 'post'], url_path='curators')
    def curators(self, request, pk=None):
        """
        GET: Возвращает список кураторов продукта.
        POST: Добавляет куратора к продукту.
        """
        product = self.get_object()

        if request.method == 'GET':
            curators = product.curators.all()
            data = [{'id': curator.id, 'username': curator.username} for curator in curators]
            return Response(data)

        if request.method == 'POST':
            user_id = request.data.get('user_id')
            if not user_id:
                return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Используем модель пользователя через settings.AUTH_USER_MODEL
                user = User.objects.get(id=user_id)
                product.curators.add(user)
                return Response({'message': f'User {user.username} added as curator.'})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class ProjectViewSet(ModelViewSet):
    """
    Вьюсет для работы с моделью Project.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """
        Добавляем возможность фильтрации по статусу и продукту.
        Например: /api/projects/?status=in_progress&product_id=1
        """
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        product_id = self.request.query_params.get('product_id')
        if status:
            queryset = queryset.filter(status=status)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset

    @action(detail=True, methods=['get', 'post'], url_path='curators')
    def curators(self, request, pk=None):
        """
        GET: Возвращает список кураторов продукта.
        POST: Добавляет куратора к продукту.
        """
        product = self.get_object()

        if request.method == 'GET':
            curators = product.curators.all()
            data = [{'id': curator.id, 'username': curator.username} for curator in curators]
            return Response(data)

        if request.method == 'POST':
            user_id = request.data.get('user_id')
            if not user_id:
                return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Используем модель пользователя через settings.AUTH_USER_MODEL
                user = User.objects.get(id=user_id)
                product.curators.add(user)
                return Response({'message': f'User {user.username} added as curator.'})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get', 'post'], url_path='members')
    def members(self, request, pk=None):
        """
        GET: Возвращает список стажеров проекта.
        POST: Добавляет стажера в проект.
        """
        project = self.get_object()

        if request.method == 'GET':
            members = project.members.all()
            data = [{'id': member.id, 'username': member.username} for member in members]
            return Response(data)

        if request.method == 'POST':
            user_id = request.data.get('user_id')
            if not user_id:
                return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Используем модель пользователя через settings.AUTH_USER_MODEL
                user = User.objects.get(id=user_id)
                project.members.add(user)
                return Response({'message': f'User {user.username} added as member.'})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
class PartnerViewSet(ModelViewSet):
    """
    Вьюсет для работы с моделью Product.
    """
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer