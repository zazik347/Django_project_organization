from django import forms

from projects.models import Project
from .models import EmployeeAssignment


class EmployeeAssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Если проект уже выбран — установи даты из проекта
        if self.instance and hasattr(self.instance, 'project'):
            project = getattr(self.instance, 'project', None)
            if project:
                self.initial['start_date'] = project.start_date
                self.initial['end_date'] = project.end_date

        # Если проект был выбран во время сохранения формы
        if 'project' in self.data:
            project_id = self.data.get('project')
            try:
                project = Project.objects.get(pk=project_id)
                self.fields['start_date'].initial = project.start_date
                self.fields['end_date'].initial = project.end_date
            except (ValueError, Project.DoesNotExist):
                pass

    class Meta:
        model = EmployeeAssignment
        fields = '__all__'



