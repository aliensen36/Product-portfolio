from django.db import models
from django.conf import settings

class Product(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Запланирован'), # продукт находится в стадии планирования, но работа ещё не началась
        ('in_development', 'В разработке'), # продукт активно разрабатывается, но ещё не готов к использованию
        ('testing', 'Тестирование'), # продукт завершён, но проходит стадию тестирования (например, бета-тест)
        ('active', 'В продакшене'), # продукт запущен и используется пользователями
        ('maintenance', 'На поддержке'), # продукт больше не развивается, но поддерживается (обновления, исправление ошибок)
        ('archived', 'Архивирован'), # продукт больше не используется и не поддерживается
        ('cancelled', 'Отменён'), # разработка продукта остановлена и не будет продолжена
    ]
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    created_at = models.DateField(blank=True, null=True, verbose_name='Дата запуска')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True,
        null=True,
        verbose_name='Статус'
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
        ('draft', 'Черновик'), # проект ещё не утверждён, находится в стадии разработки концепции
        ('planned', 'Запланирован'), # проект утверждён, но ещё не начат
        ('in_progress', 'В процессе'), # проект находится в активной разработке
        ('on_hold', 'Приостановлен'), # работа временно остановлена (например, из-за нехватки ресурсов)
        ('under_review', 'На проверке'), # проект завершён, но проходит проверку или оценку
        ('completed', 'Завершён'), # проект успешно выполнен и завершён
        ('cancelled', 'Отменён'), # проект закрыт без завершения
        ('archived', 'Архивирован'), # проект завершён или отменён, больше не активен
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
