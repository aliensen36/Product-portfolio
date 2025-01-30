from rest_framework import serializers
from .models import Product, Project


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.
    """
    customers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Список ID заказчиков
    curators = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Список ID кураторов
    projects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Список ID связанных проектов

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'created_at',
            'status',
            'customers',
            'curators',
            'projects',
        )


class ProjectSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Project.
    """
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # ID продукта
    curators = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Список ID кураторов
    interns = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Список ID стажёров

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'product',
            'description',
            'start_date',
            'end_date',
            'status',
            'curators',
            'interns',
        )
