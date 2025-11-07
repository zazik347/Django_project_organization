from django import forms
from .models import Constructor


class ConstractorForm(forms.ModelForm):
    class Meta:
        model = Constructor
        fields = ['worker_constr', 'department', 'photo', 'role', 'projects']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }
