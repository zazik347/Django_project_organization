from django.db import models
# from contracts.models import Contract
from employees.models import Employee, EmployeeAssignment
from equipment.models import Equipment


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    # contract = models.ForeignKey('contracts.Contract', on_delete=models.CASCADE, related_name='projects')
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='managed_projects')
    employees_more = models.ManyToManyField("employees.Employee", related_name='assigned_projects', blank=True, verbose_name='Привлечь сотрудников')
    new_employees_more = models.ManyToManyField("employees.Employee", through='ProjectEmployee', related_name='new_employees_more', blank=True,
                                            verbose_name='Привлечь сотрудников')
    equipment_chosen = models.ManyToManyField("equipment.Equipment", related_name='project_equipment', through="ProjectEquipment")
    # Связь с EmployeeAssignment
    assignments = models.ManyToManyField(
        "employees.Employee",
        through='employees.EmployeeAssignment',
        related_name='assigned_projects_money'
    )
    subcontractors = models.ManyToManyField(
        'subcontractors.Subcontractor',
        through='subcontractors.SubcontractorAssignment',
        related_name='subcontract_projects',
        blank=True
    )

    def __str__(self):
        return self.title

class ProjectEmployee(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name='employees')
    employee = models.ForeignKey("employees.Employee", on_delete=models.CASCADE)
    role = models.CharField(max_length=255)  # роль сотрудника в проекте

    def __str__(self):
        return f"{self.employee.full_name} - {self.role} в {self.project.title}"

    class Meta:
        verbose_name = 'Сотрудник проекта'
        verbose_name_plural = 'Сотрудники проекта'


class ProjectEquipment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='equipment')
    equipment = models.ForeignKey("equipment.Equipment", on_delete=models.CASCADE)
    usage_description = models.TextField(blank=True)  # описание использования оборудования

    def __str__(self):
        return f"{self.equipment.name} используется в {self.project.title}"
