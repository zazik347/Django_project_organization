from django import forms
from .models import Equipment, EquipmentTransfer
from departments.models import Department
from employees.models import Employee

class IssueEquipmentForm(forms.Form):
    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.filter(status='in_stock'),
        label="Оборудование на складе",
        empty_label="Выберите оборудование"
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label="Выдать отделу"
    )
    responsible_person = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        label="Ответственное лицо",
        widget=forms.Select(attrs={'class': 'select2'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Комментарии"
    )

