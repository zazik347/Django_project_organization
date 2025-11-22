from django.contrib import admin
from django.utils.html import format_html

from constructors.models import Constructor, ConstructorRole, ConstrDepartment

@admin.register(ConstructorRole)
class ConstructorRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_head')
    search_fields = ('name',)

@admin.register(Constructor)
class ConstructorAdmin(admin.ModelAdmin):
    readonly_fields = ['photo_preview']
    list_display = ('worker_constr', 'department', 'role', 'get_certificates_preview', 'patent_count')
    search_fields = ('full_name',)
    list_filter = ('role',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.photo.url)
        return "Нет фото"
    photo_preview.short_description = 'Превью фото'
    photo_preview.allow_tags = True

    def get_certificates_preview(self, obj):
        if obj.certificates:
            return obj.certificates[:60] + "..." if len(obj.certificates) > 60 else obj.certificates
        return "—"
    get_certificates_preview.short_description = "Патенты и свидетельства"

    fieldsets = (
        ('Основная информация', {
            'fields': ('worker_constr', 'department', 'role', 'photo')
        }),
        ('Авторские свидетельства', {
            'fields': ('certificates', 'patent_count'),
            'classes': ('collapse',),
            'description': 'Укажите патенты, изобретения, авторские свидетельства'
        }),
    )

@admin.register(ConstrDepartment)
class ConstrDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
