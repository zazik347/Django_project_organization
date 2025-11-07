from django.contrib import admin

from employees.admin import EmployeeAssignmentInline
from projects.models import Project, ProjectEmployee, ProjectEquipment
from subcontractors.models import SubcontractorAssignment

# Register your models here.
# admin.site.register(Project)
# admin.site.register(ProjectEmployee)
admin.site.register(ProjectEquipment)

# Регистрация модели связи
@admin.register(ProjectEmployee)
class ProjectEmployeeAdmin(admin.ModelAdmin):
    list_display = ('project', 'employee', 'role')
    list_filter = ('project',)
    search_fields = ('employee__full_name', 'role')  # поиск по связанным полям

# Inline-форма для связи ProjectEmployee
class ProjectEmployeeInline(admin.TabularInline):  # или StackedInline
    model = ProjectEmployee
    extra = 1  # количество пустых форм для добавления новых связей

# Inline для подрядчиков
class SubcontractorAssignmentInline(admin.TabularInline):
    model = SubcontractorAssignment
    extra = 1
    fields = ('subcontractor', 'work_description', 'cost')
    verbose_name = "Назначение подрядчика"
    verbose_name_plural = "Подрядчики проекта"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [EmployeeAssignmentInline, SubcontractorAssignmentInline,]
    list_display = ('title', 'start_date', 'end_date')

    class Media:
        js = ('employees/js/admin.js',)


