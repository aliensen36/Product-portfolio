from rest_framework import serializers
from .models import *
from django.conf import settings


class ProductSerializer(serializers.ModelSerializer):
    # Сериализуем ManyToMany поля (например, владельцы, кураторы, сферы)
    owners = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    curators = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    spheres = serializers.PrimaryKeyRelatedField(queryset=Sphere.objects.all(), many=True)

    # Мы можем добавить дополнительные поля для отображения статусов и моделей продаж
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    sales_model_display = serializers.CharField(source='get_sales_model_display', read_only=True)
    logo = serializers.SerializerMethodField()

    def get_logo(self, obj):
        if obj.logo:
            return obj.logo.url  # автоматически создаст абсолютный URL
        return None


    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'created_at', 'status', 'status_display', 'owners', 'curators', 'spheres',
            'sales_model', 'sales_model_display', 'logo'
        ]
        read_only_fields = ['status_display', 'sales_model_display']


class ProjectSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Project.
    """
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # ID продукта
    curators = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Список ID кураторов
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Список ID стажёров

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
            'members',
        )

class PartnerSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Partner.
    """
    logo = serializers.SerializerMethodField()

    def get_logo(self, obj):
        if obj.logo:
            return obj.logo.url  # автоматически создаст абсолютный URL
        return None
    
    class Meta:
        model = Partner
        fields = (
            'id',
            'name',
            'logo',
            'url',
        )