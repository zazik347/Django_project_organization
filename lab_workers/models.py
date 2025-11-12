from django.db import models
from employees.models import Employee


class LabWorker(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, blank=True)  # специализация

    def __str__(self):
        return f"Лаборант: {self.employee.full_name}"
