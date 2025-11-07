from django.contrib import admin
from employees.models import Employee, EmployeeAssignment
from employees.forms import EmployeeAssignmentForm
from django import forms

@admin.register(Employee)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'department', 'hourly_rate')
    search_fields = ('full_name',)
    list_filter = ('department',)
    list_editable = ('hourly_rate',)

class EmployeeAssignmentInline(admin.TabularInline):
    model = EmployeeAssignment
    extra = 1
    fields = ('employee', 'start_date', 'end_date')
    form = EmployeeAssignmentForm  # чтобы работал JS



@admin.register(EmployeeAssignment)
class EmployeeAssignmentAdmin(admin.ModelAdmin):
    form = EmployeeAssignmentForm
    list_display = ('employee', 'project', 'start_date', 'end_date')

    class Media:
        js = ('employees/js/admin.js',)
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if obj and hasattr(obj, 'project'):
            project = getattr(obj, 'project', None)
            if project:
                form.base_fields['start_date'].initial = project.start_date
                form.base_fields['end_date'].initial = project.end_date

        return form

class EmployeeAssignmentForm(forms.ModelForm):
    class Meta:
        model = EmployeeAssignment
        fields = '__all__'  # или перечисли поля
