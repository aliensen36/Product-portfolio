from django.contrib import admin
from .models import Product, Project
from django.utils.html import format_html

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    filter_horizontal = ('owners', 'curators')
    readonly_fields = ('get_projects',)

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

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'start_date', 'end_date')
    search_fields = ('name',)
    list_filter = ('start_date', 'end_date', 'product')
    filter_horizontal = ('curators', 'members')

admin.site.register(Product, ProductAdmin)
admin.site.register(Project, ProjectAdmin)