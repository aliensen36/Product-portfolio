from django.contrib import admin
from .models import *
from django.utils.html import format_html


class ProductAdmin(admin.ModelAdmin):
    list_display = ('display_logo', 'name', 'formatted_created_at')
    list_display_links = ('display_logo', 'name')
    search_fields = ('name', 'created_at')
    list_filter = ('created_at',)
    filter_horizontal = ('owners', 'curators', 'partners', 'spheres')
    readonly_fields = ('get_projects', 'display_logo')
    fieldsets = (
        ('Основные сведения', {
            'fields': ('name', 'display_logo', 'logo', 'description', 'created_at', 'status', 'sales_model')
        }),
        ('Заказчики, кураторы и партнеры', {
            'fields': ('owners', 'curators', 'partners'),
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


class ProjectStageInline(admin.TabularInline):
    model = ProjectStage
    extra = 0
class ProjectRoleInline(admin.TabularInline):
    model = ProjectRole
    extra = 0
    verbose_name = 'Роль участника'
    verbose_name_plural = 'Роли участников'

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('display_logo', 'name', 'product')
    list_display_links = ('display_logo', 'name', 'product')
    search_fields = ('name', 'product')
    list_filter = ('start_date', 'end_date', 'product')
    filter_horizontal = ('curators', 'members', 'partners')
    readonly_fields = ('stages_list', 'display_logo', 'members_and_roles_list')
    inlines = [ProjectStageInline, ProjectRoleInline]

    fieldsets = (
        ('Основные сведения', {
            'fields': ('name', 'display_logo', 'logo', 'product', 'description', 'principles', 'status', 'start_date', 'end_date')
        }),
        ('Этапы проекта', {
            'fields': ('stages_list',),
        }),
        ('Кураторы, участники и партнеры', {
            'fields': ('curators', 'members', 'partners'),
        }),
        ('Роли участников', {
            'fields': ('members_and_roles_list',)
        }),
    )

    def display_logo(self, obj):
        """Отображает логотип в админке"""
        if obj.logo and obj.logo.url:
            return format_html('<img src="{}" style="width: 100px; height: 60px;" alt="Логотип">', obj.logo.url)
        return "Логотип отсутствует"

    display_logo.short_description = 'Логотип'

    def stages_list(self, obj):
        # Получаем связанные этапы для проекта
        stages = obj.stages.all()
        # Форматируем вывод: дата начала и окончания этапа, если end_date существует
        return format_html('<br>'.join([
            f'{stage.start_date.strftime("%d.%m.%Y")} - {stage.end_date.strftime("%d.%m.%Y") if stage.end_date else ""}    –    {stage.name}'
            for stage in stages
        ]))

    stages_list.short_description = 'Этапы'

    def members_and_roles_list(self, obj):
        # Получаем связанные роли участников для проекта
        project_roles = obj.project_roles.select_related('member', 'role')
        # Форматируем вывод в виде: "Иван Иванов – Бекендер"
        return format_html('<br>'.join([
            f'{role.member} – {role.role.name}' for role in project_roles
        ]))

    members_and_roles_list.short_description = 'Роли участников'



class SphereAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('display_logo', 'name')
    list_display_links = ('display_logo', 'name')
    search_fields = ('name',)
    readonly_fields = ('display_logo',)
    fieldsets = (
        ('Основные сведения', {
            'fields': ('name', 'display_logo', 'logo', 'url')
        }),
    )

    def display_logo(self, obj):
        """Отображает логотип в админке"""
        if obj.logo and obj.logo.url:
            return format_html('<img src="{}" style="width: 100px; height: 60px;" alt="Логотип">', obj.logo.url)
        return "Логотип отсутствует"

    display_logo.short_description = 'Логотип'


class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SalesModelAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProjectStageAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ('member', 'role', 'project')
    search_fields = ('member__username', 'role__name', 'project__name')
    list_filter = ('role', 'project')
    autocomplete_fields = ('member', 'role', 'project')


admin.site.register(Product, ProductAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Sphere, SphereAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(ProductStatus, ProductStatusAdmin)
admin.site.register(ProjectStatus, ProjectStatusAdmin)
admin.site.register(SalesModel, SalesModelAdmin)
admin.site.register(ProjectStage, ProjectStageAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(ProjectRole, ProjectRoleAdmin)

