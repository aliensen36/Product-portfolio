from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    created_at = models.DateField(blank=True, null=True, verbose_name='Дата запуска')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='projects', verbose_name='Продукт')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(blank=True, null=True, verbose_name='Дата завершения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
