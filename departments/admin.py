from django.contrib import admin
from departments.models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # list_display = ('name', 'head')
    search_fields = ('name',)
