from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from departments.models import Department

class Employee(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    department = models.ForeignKey('departments.Department', null=True, blank=True, related_name='employees', on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name='Дата начала работы', default=timezone.now)
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Часовая ставка',
        default=0
    )

    def __str__(self):
        return self.full_name

class EmployeeAssignment(models.Model):
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='employee_assignments')
    start_date = models.DateField(verbose_name='Дата начала работы в проекте')
    end_date = models.DateField(verbose_name='Дата окончания работы в проекте', null=True, blank=True)


    @property
    def duration_days(self):
        if self.end_date:
            return (self.end_date - self.start_date).days
        return (date.today() - self.start_date).days

    @property
    def total_cost(self):
        return self.duration_days * self.employee.hourly_rate * 8  # 8 часов в день

    def __str__(self):
        return f"{self.employee} - {self.project} ({self.start_date} до {self.end_date or 'текущий'})"
