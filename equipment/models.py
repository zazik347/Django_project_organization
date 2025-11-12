from datetime import date

from django.db import models
from departments.models import Department
from employees.models import Employee



class Equipment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # owner_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name


class EquipmentAssignment(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='assignments')
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    assigned_date = models.DateField()  # Дата выдачи
    returned_date = models.DateField(null=True, blank=True)  # Дата возврата

    def __str__(self):
        return f"{self.equipment.name} -  {self.assigned_date}"

    @property
    def is_active(self):
        # Активное распределение — если ещё не возвращено
        return self.returned_date is None or self.returned_date > date.today()
