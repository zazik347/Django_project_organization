from django.contrib import admin
from django.utils.html import format_html

from avtomatizations.models import AutomationEngineer, AutomationRole, AutomationDepartment


@admin.register(AutomationRole)
class AutomationRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_head')
    search_fields = ('name',)

@admin.register(AutomationEngineer)
class AutomationEngineerAdmin(admin.ModelAdmin):
    readonly_fields = ['photo_preview']
    list_display = ('worker_avt', 'department', 'role')
    search_fields = ('full_name',)
    list_filter = ('role',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.photo.url)
        return "Нет фото"
    photo_preview.short_description = 'Превью фото'
    photo_preview.allow_tags = True

@admin.register(AutomationDepartment)
class AutomationDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
