from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from django.conf import settings

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class SphereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sphere
        fields = ['id', 'name', 'description']


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'name', 'logo', 'url']


class ProductSerializer(serializers.ModelSerializer):
    owners = UserSerializer(many=True, read_only=True)
    curators = UserSerializer(many=True, read_only=True)
    partners = PartnerSerializer(many=True, read_only=True)
    spheres = SphereSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'created_at', 'status', 'owners', 'curators',
            'partners', 'spheres', 'sales_model', 'logo'
        ]


class ProjectSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # ID продукта
    members = UserSerializer(many=True, read_only=True)
    curators = UserSerializer(many=True, read_only=True)
    partners = PartnerSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'product', 'description', 'start_date', 'end_date',
            'status', 'curators', 'members', 'partners'
        ]
