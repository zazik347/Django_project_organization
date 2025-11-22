import os
import uuid
import datetime

from django.db import models
from django.utils.html import format_html

class ConstructorRole(models.Model):
    name = models.CharField(max_length=100, verbose_name='Должность')
    is_head = models.BooleanField(default=False, verbose_name='Начальник')

    def __str__(self):
        return self.name

def engineer_constr_photo_path(instance, filename):
    # Извлекаем расширение файла
    ext = filename.split('.')[-1]
    # Генерируем уникальное имя файла
    unique_filename = f"{uuid.uuid4()}_{instance.worker_constr.id}.{ext}"
    return os.path.join('constractors', 'media', 'foto_card', unique_filename)

class Constructor(models.Model):
    worker_constr = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, verbose_name='Сотрудник', null=True, blank=True )
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, verbose_name='Отдел', null=True)
    role = models.ForeignKey(ConstructorRole, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Должность')
    photo = models.ImageField(upload_to=engineer_constr_photo_path, blank=True, null=True)
    projects = models.ManyToManyField('projects.Project', related_name='constructors', verbose_name='Проекты', blank=True)
    certificates = models.TextField(
        blank=True,
        null=True,
        verbose_name="Авторские свидетельства",
        help_text="Перечислите авторские свидетельства, патенты, изобретения"
    )

    patent_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество авторских свидетельств",
        help_text="Введите число — сколько патентов или свидетельств у конструктора"
    )

    def experience(self):
        today = datetime.date.today()
        years = today.year - self.worker_constr.start_date.year
        months = today.month - self.worker_constr.start_date.month
        days = today.day - self.worker_constr.start_date.day
        if days < 0:
            months -= 1
            days += 30  # приблизительно
        if months < 0:
            years -= 1
            months += 12

        return f"{years} лет, {months} месяцев"

    def __str__(self):
        return self.worker_constr.full_name if self.worker_constr else 'Не определён'

    def photo_preview(self):
        if self.photo:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', self.photo.url)
        return "Нет фото"
    photo_preview.short_description = 'Превью фото'

class ConstrDepartment(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название отдела')
    description = models.TextField(blank=True, verbose_name='Описание')
    workers = models.ManyToManyField(Constructor, related_name='design_departments', verbose_name='Сотрудники')


    def __str__(self):
        return self.name
