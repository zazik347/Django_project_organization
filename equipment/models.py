from datetime import date

from django.db import models
from departments.models import Department
from employees.models import Employee



class Equipment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    serial_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='Серийный номер')
    purchase_date = models.DateField(
        verbose_name='Дата покупки',
        null=True,
        blank=True,
    )
    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Стоимость',
        default=0
    )
    condition = models.CharField(
        max_length=50,
        choices=[
            ('good', 'Исправно'),
            ('repair', 'Требует ремонта'),
            ('broken', 'Вышло из строя'),
        ],
        default='good',
        verbose_name='Состояние'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('in_stock', 'На складе'),
            ('in_use', 'В использовании'),
            ('in_repair', 'В ремонте'),
        ],
        default='in_stock',
        verbose_name='Статус'
    )
    current_department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Текущий отдел',
        help_text='Отдел, который сейчас использует оборудование'
    )
    notes = models.TextField(blank=True, null=True, verbose_name='Примечания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'

    # === Методы для работы со складом ===

    def mark_as_issued(self, to_department, person, notes=""):
        """
        Выдать оборудование отделу (со склада)
        """
        from .models import EquipmentTransfer
        transfer = EquipmentTransfer.objects.create(
            equipment=self,
            from_department=None,
            to_department=to_department,
            responsible_person=person,
            notes=notes,
            transfer_date=date.today()
        )
        self.current_department = to_department
        self.status = 'in_use'
        self.save()
        return transfer

    def mark_as_returned(self, from_department, person, notes=""):
        """
        Вернуть оборудование на склад
        """
        from .models import EquipmentTransfer
        transfer = EquipmentTransfer.objects.create(
            equipment=self,
            from_department=from_department,
            to_department=None,
            responsible_person=person,
            notes=notes,
            transfer_date=date.today()
        )
        self.current_department = None
        self.status = 'in_stock'
        self.save()
        return transfer

    def transfer_between_departments(self, from_dept, to_dept, person, notes=""):
        """
        Передать оборудование между отделами
        """
        from .models import EquipmentTransfer
        transfer = EquipmentTransfer.objects.create(
            equipment=self,
            from_department=from_dept,
            to_department=to_dept,
            responsible_person=person,
            notes=notes,
            transfer_date=date.today()
        )
        self.current_department = to_dept
        self.save()
        return transfer

    @property
    def is_in_stock(self):
        return self.status == 'in_stock'

    @property
    def is_in_use(self):
        return self.status == 'in_use'





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

class EquipmentTransfer(models.Model):
    equipment = models.ForeignKey(
        'Equipment',
        on_delete=models.CASCADE,
        related_name='transfers',
        verbose_name='Оборудование'
    )
    from_department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipment_sent',
        verbose_name='Отдел-отправитель'
    )
    to_department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipment_received',
        verbose_name='Отдел-получатель'
    )
    transfer_date = models.DateField(default=date.today, verbose_name='Дата передачи')
    responsible_person = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name='Ответственное лицо'
    )
    notes = models.TextField(blank=True, null=True, verbose_name='Комментарии')

    def __str__(self):
        if not self.from_department and self.to_department:
            return f"✅ Выдано: {self.equipment.name} → {self.to_department}"
        elif self.from_department and not self.to_department:
            return f"📦 Возвращено: {self.equipment.name} → Склад"
        elif self.from_department and self.to_department:
            return f"🔁 Передано: {self.equipment.name} {self.from_department} → {self.to_department}"
        return f"{self.equipment.name} — Передача"

    class Meta:
        verbose_name = 'Передача оборудования'
        verbose_name_plural = 'Передачи оборудования'
        ordering = ['-transfer_date']
