from django import forms
from .models import AutomationEngineer


class EngineerForm(forms.ModelForm):
    class Meta:
        model = AutomationEngineer
        fields = ['worker_avt', 'department', 'photo', 'role', 'projects']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }
