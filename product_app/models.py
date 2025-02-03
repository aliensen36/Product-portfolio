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

class Product(models.Model):
    STATUS_CHOICES = [
        ('idea', 'идея'),
        ('recruitment ongoing', 'идет набор'),
        ('MVP development', 'разработка MVP'),
        ('MVP ready', 'MVP готов'),
        ('first sales', 'первые продажи'),
        ('early growth', 'ранний рост'),
        ('scaling', 'масштабирование'),
        ('late growth', 'поздний рост'),
        ('frozen', 'заморожен'),
        ('closed', 'закрыт'),
    ]
    SALES_CHOICES = [
        ('B2B', 'B2B'),
        ('B2C', 'B2C'),
        ('B2G', 'B2G'),
        ('C2C', 'C2C'),
        ('B2B2C', 'B2B2C'),
    ]
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    created_at = models.DateField(blank=True, null=True, verbose_name='Дата запуска')
    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        blank=True,
        null=True,
        verbose_name='Статус',
        help_text = 'Выберите текущий статус продукта. Например, "идея" или "разработка MVP".'
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
    spheres = models.ManyToManyField(
        Sphere,
        related_name='products',
        blank=True,
        verbose_name='Сферы',
        help_text='Выберите одну или несколько сфер, к которым относится продукт.'
    )
    sales_model = models.CharField(
        max_length=40,
        choices=SALES_CHOICES,
        blank=True,
        null=True,
        verbose_name='Модель продаж',
        help_text='Выберите модель продаж продукта, например, B2B или C2C.'
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


class Project(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('planned', 'Запланирован'),
        ('in_progress', 'В процессе'),
        ('on_hold', 'Приостановлен'),
        ('under_review', 'На проверке'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
        ('archived', 'Архивирован'),
    ]
    name = models.CharField(max_length=255, verbose_name='Название')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='projects', verbose_name='Продукт')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(blank=True, null=True, verbose_name='Дата завершения')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True,
        null=True,
        verbose_name='Статус'
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

class Partner(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    logo = models.FileField(
        upload_to=upload_to,
        validators=[validate_logo_file, validate_logo_size],
        blank=True,
        null=True,
        verbose_name='Логотип',
        help_text = 'Загрузите изображение в формате JPEG или PNG размером не более 2 МБ'
    )
    url = models.URLField()
        
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'
