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


class ProductStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStatus
        fields = ['id', 'name', 'description']


class ProjectStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStage
        fields = ['id', 'project', 'name', 'start_date', 'end_date']
        read_only_fields = ['id']  # Поле `id` будет доступно только для чтения


class SalesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesModel
        fields = ['id', 'name', 'description']  # Поля, которые будут сериализованы
        read_only_fields = ['id']  # Поле id доступно только для чтения


class ProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatus
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class ProjectRoleSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.get_full_name', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = ProjectRole
        fields = ['id', 'member', 'member_name', 'role', 'role_name', 'project', 'project_name']


