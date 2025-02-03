from django.contrib import admin
from .models import *
from django.utils.html import format_html


class ProductAdmin(admin.ModelAdmin):
    list_display = ('display_logo', 'name', 'formatted_created_at')
    list_display_links = ('display_logo', 'name')
    search_fields = ('name', 'created_at')
    list_filter = ('created_at',)
    filter_horizontal = ('owners', 'curators', 'spheres')
    readonly_fields = ('get_projects', 'display_logo')
    fieldsets = (
        ('Основные сведения', {
            'fields': ('name', 'display_logo', 'logo', 'description', 'created_at', 'status', 'sales_model')
        }),
        ('Заказчики и кураторы', {
            'fields': ('owners', 'curators'),
        }),
        ('Сферы', {
            'fields': ('spheres',),
        }),
    )

    def formatted_created_at(self, obj):
        """Возвращает дату в формате '01.02.2025'"""
        if obj.created_at:
            return obj.created_at.strftime('%d.%m.%Y')
        return 'Не указана'

    formatted_created_at.short_description = 'Дата запуска'

    def get_projects(self, obj):
        """Возвращает список связанных проектов с ссылками на редактирование"""
        projects = obj.projects.all()
        if not projects:
            return "Нет связанных проектов"
        return format_html(
            "<br>".join(
                [
                    f'<a href="/admin/{project._meta.app_label}/{project._meta.model_name}/{project.id}/change/">{project.name}</a>'
                    for project in projects
                ]
            )
        )
    get_projects.short_description = 'Проекты'

    def display_logo(self, obj):
        """Отображает логотип в админке"""
        if obj.logo and obj.logo.url:
            return format_html('<img src="{}" style="width: 100px; height: 60px;" alt="Логотип">', obj.logo.url)
        return "Логотип отсутствует"
    display_logo.short_description = 'Логотип'


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'start_date', 'end_date')
    search_fields = ('name',)
    list_filter = ('start_date', 'end_date', 'product')
    filter_horizontal = ('curators', 'members')

class SphereAdmin(admin.ModelAdmin):
    list_display = ('name',)

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo', 'display_logo', 'url', 'formatted_created_at')
    list_display_links = ('display_logo', 'name')
    search_fields = ('name',)
    readonly_fields = ('url', 'display_logo')
    fieldsets = (
        ('Основные сведения', {
            'fields': ('name', 'display_logo', 'logo',)
        }),
    )

    def formatted_created_at(self, obj):
        """Возвращает дату в формате '01.02.2025'"""
        if obj.created_at:
            return obj.created_at.strftime('%d.%m.%Y')
        return 'Не указана'

    formatted_created_at.short_description = 'Дата запуска'

    def display_logo(self, obj):
        """Отображает логотип в админке"""
        if obj.logo and obj.logo.url:
            return format_html('<img src="{}" style="width: 100px; height: 60px;" alt="Логотип">', obj.logo.url)
        return "Логотип отсутствует"
    display_logo.short_description = 'Логотип'

admin.site.register(Product, ProductAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Sphere, SphereAdmin)
admin.site.register(Partner, PartnerAdmin)