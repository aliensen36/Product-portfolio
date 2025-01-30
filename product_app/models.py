from django.db import models
from django.conf import settings

class Product(models.Model):
    STATUS_CHOICES = [
        ('idea', 'идея'), # продукт находится в стадии планирования, но работа ещё не началась
        ('recruitment ongoing', 'идет набор'), # продукт активно разрабатывается, но ещё не готов к использованию
        ('MVP development', 'разработка MVP'), # продукт завершён, но проходит стадию тестирования (например, бета-тест)
        ('MVP ready', 'MVP готов'), # продукт запущен и используется пользователями
        ('first sales', 'Первые продажи'), # продукт больше не развивается, но поддерживается (обновления, исправление ошибок)
        ('early growth', 'ранний доступ'), # продукт больше не используется и не поддерживается
        ('scaling', 'масштабирование'), # разработка продукта остановлена и не будет продолжена
        ('late growth', 'поздний доступ'), # разработка продукта остановлена и не будет продолжена
        ('frozen', 'заморожен'), # разработка продукта остановлена и не будет продолжена
        ('closed', 'закрыт'), # разработка продукта остановлена и не будет продолжена
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
    SPHERE_CHOICES = [
        ('process automation', 'автоматизация процессов'), #
        ('online marketing', 'онлайн-маркетинг'), #
        ('travel', 'путешествия'), #
        ('entertainment', 'развлечения'), #
        ('tools', 'инструменты'), #
    ]
    sphere = models.CharField(
        max_length=20,
        choices=SPHERE_CHOICES,
        blank=True,
        null=True,
        verbose_name='Сфера'    
    )
    SALES_CHOICES = [
        ('B2B','B2B'), # business to business
        ('B2C', 'B2C'), # business to consumer
        ('B2G', 'B2G'), # business to government
        ('C2C', 'C2C'), # consumer to consumer
        ('B2B2C', 'B2B2C'), # business to business to consumer
    ]
    sales_model = models.CharField(
        max_length=20,
        choices=SALES_CHOICES,
        blank=True,
        null=True,
        verbose_name='Модель продаж'    
    )
    logo = models.FileField(
        upload_to='upload_logo',
        blank=True,
        null=True,
        verbose_name='Логотип'
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
