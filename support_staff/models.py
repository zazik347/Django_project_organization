from django.db import models
from employees.models import Employee


class SupportStaff(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)  # роль или должность

    def __str__(self):
        return f"Персонал: {self.employee.full_name}"
