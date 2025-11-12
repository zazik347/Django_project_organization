from django.db import models



class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название отдела')
    # head = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_departments')

    def __str__(self):
        return self.name
