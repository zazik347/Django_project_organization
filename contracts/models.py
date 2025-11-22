from datetime import date

from django.db import models
from employees.models import Employee
# from projects.models import Project


class Contract(models.Model):
    client = models.CharField(max_length=255)
    number = models.CharField(max_length=50)
    # Убираем primary_project, добавляем projects
    projects = models.ManyToManyField(
        'projects.Project',
        related_name='contracts',
        blank=True,
        verbose_name='Проекты по договору'
    )
    # primary_project = models.ForeignKey(
    #     'projects.Project',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='primary_contract',
    #     verbose_name='Основной проект'
    # )
    start_date = models.DateField(default=date.fromisoformat('2025-10-20'))
    end_date = models.DateField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    manager =  models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='managed_contracts')

    def __str__(self):
        return f"Договор с {self.client} - {self.number}"

class ContractEmployee(models.Model):
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, related_name='employees')
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE)
    role = models.CharField(max_length=255)  # роль сотрудника в договоре

    def __str__(self):
        return f"{self.employee.full_name} - {self.role} в {self.contract.client}"
