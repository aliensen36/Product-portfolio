from django.contrib import admin
from .models import Product, Project

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'start_date', 'end_date')
    search_fields = ('name',)
    list_filter = ('start_date', 'end_date', 'product')

admin.site.register(Product, ProductAdmin)
admin.site.register(Project, ProjectAdmin)