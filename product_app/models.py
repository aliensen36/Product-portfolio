import os
import mimetypes
from django.db import models
from django.conf import settings
from datetime import datetime
from unidecode import unidecode
from django.core.exceptions import ValidationError


def upload_to(instance, filename):
    # Получаем расширение файла
    ext = filename.split('.')[-1]

    # Преобразуем имя продукта в ASCII, чтобы избежать русских букв
    safe_name = unidecode(instance.name)

    # Генерируем имя файла
    filename = f"{safe_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"

    # Возвращаем путь, где будет сохранен файл
    return os.path.join('logos', filename)

def validate_logo_file(value):
    # Проверяем MIME-тип
    valid_mime_types = ['image/jpeg', 'image/png', 'image/svg+xml']
    mime_type, _ = mimetypes.guess_type(value.name)
    if mime_type not in valid_mime_types:
        raise ValidationError(f"Неподдерживаемый тип файла. Допустимы только изображения.")

def validate_logo_size(value):
    # Устанавливаем максимальный размер файла в байтах
    max_size_mb = 2
    max_size = max_size_mb * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(f"Размер файла превышает {max_size_mb} МБ. Загрузите файл меньшего размера.")


class Sphere(models.Model):
    name = models.CharField(max_length=40, unique=True, verbose_name='Название сферы')
    description = models.TextField(blank=True, null=True, verbose_name='Описание сферы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сфера'
        verbose_name_plural = 'Сферы'


class Partner(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    logo = models.FileField(
        upload_to=upload_to,
        validators=[validate_logo_file, validate_logo_size],
        blank=True,
        null=True,
        verbose_name='Логотип',
        help_text='Загрузите изображение в формате JPEG или PNG размером не более 2 МБ'
    )
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'


class ProductStatus(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Статус продукта"
        verbose_name_plural = "Статусы продуктов"

    def __str__(self):
        return self.name


class SalesModel(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = 'Модель продаж'
        verbose_name_plural = 'Модели продаж'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    created_at = models.DateField(blank=True, null=True, verbose_name='Дата запуска')
    status = models.ForeignKey(
        ProductStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Статус"
    )
    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='products_as_owner',
        verbose_name='Заказчики'
    )
    curators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='products_as_curator',
        verbose_name='Кураторы'
    )
    partners = models.ManyToManyField(
        Partner,
        related_name='products_as_partner',
        blank=True,
        verbose_name='Партнеры',
        help_text='Добавьте партнера(ов) Продукта.'
    )
    spheres = models.ManyToManyField(
        Sphere,
        related_name='products_as_sphere',
        blank=True,
        verbose_name='Сферы',
        help_text='Добавьте сферу(ы), к которой(ым) относится Продукт.'
    )
    sales_model = models.ForeignKey(
        SalesModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Модель продаж',
        help_text='Выберите модель продаж, например, B2B или C2C.'
    )
    logo = models.FileField(
        upload_to=upload_to,
        validators=[validate_logo_file, validate_logo_size],
        blank=True,
        null=True,
        verbose_name='Логотип',
        help_text = 'Загрузите изображение в формате JPEG или PNG размером не более 2 МБ'
    )

    def get_projects(self):
        """Возвращает список связанных проектов"""
        return self.projects.all()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProjectStatus(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Статус проекта"
        verbose_name_plural = "Статусы проектов"

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class ProjectRole(models.Model):
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='project_roles',
        verbose_name='Участник'
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='project_roles',
        verbose_name='Роль'
    )
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='project_roles',
        verbose_name='Проект'
    )

    class Meta:
        verbose_name = 'Роль участника в проекте'
        verbose_name_plural = 'Роли участников в проекте'
        unique_together = ('member', 'project')  # Уникальная пара участник-проект

    def __str__(self):
        return f"{self.member} – {self.role.name}"


class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='projects', verbose_name='Продукт')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    principles = models.TextField(blank=True, null=True, verbose_name='Принципы работы')
    start_date = models.DateField(blank=True, null=True, verbose_name='Дата запуска')
    end_date = models.DateField(blank=True, null=True, verbose_name='Дата завершения')
    status = models.ForeignKey(
        ProjectStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Статус"
    )
    curators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='projects_as_curator',
        verbose_name='Кураторы'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='projects_as_member',
        verbose_name='Стажёры'
    )
    partners = models.ManyToManyField(
        Partner,
        related_name='projects_as_partner',
        blank=True,
        verbose_name='Партнеры',
        help_text='Добавьте партнера(ов) Продукта.'
    )
    logo = models.FileField(
        upload_to=upload_to,
        validators=[validate_logo_file, validate_logo_size],
        blank=True,
        null=True,
        verbose_name='Логотип',
        help_text='Загрузите изображение в формате JPEG или PNG размером не более 2 МБ'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class ProjectStage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='stages',
        verbose_name='Проект'
    )
    name = models.CharField(max_length=255, verbose_name='Название этапа')
    start_date = models.DateField(verbose_name='Дата начала этапа', blank=True, null=True)
    end_date = models.DateField(verbose_name='Дата окончания этапа', blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.project.name})'

    class Meta:
        verbose_name = 'Этап проекта'
        verbose_name_plural = 'Этапы проектов'


