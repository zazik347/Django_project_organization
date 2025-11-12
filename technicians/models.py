from django.db import models
from employees.models import Employee


class Technician(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    equipment_skills = models.TextField(blank=True)  # оборудование, которое обслуживает

    def __str__(self):
        return f"Техник: {self.employee.full_name}"
