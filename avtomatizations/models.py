import datetime
import os
import uuid
from django.db import models
from django.utils.html import format_html

class AutomationRole(models.Model):
    name = models.CharField(max_length=100, verbose_name='Должность')
    is_head = models.BooleanField(default=False, verbose_name='Начальник')

    def __str__(self):
        return self.name

def engineer_photo_path(instance, filename):
    # Извлекаем расширение файла
    ext = filename.split('.')[-1]
    # Генерируем уникальное имя файла
    unique_filename = f"{uuid.uuid4()}_{instance.worker_avt.id}.{ext}"
    return os.path.join('avtomatization', 'media', 'foto_card', unique_filename)


class AutomationEngineer(models.Model):
    worker_avt = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, verbose_name='Сотрудник', null=True)
    # full_name = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, max_length=255, verbose_name='ФИО', related_name='employee_avt_eng')
    # birth_date = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, null=True, verbose_name='Дата рождения', related_name='birth_date_avt_eng')
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, verbose_name='Отдел')
    role = models.ForeignKey(AutomationRole, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Должность')
    photo = models.ImageField(upload_to=engineer_photo_path, blank=True, null=True)
    projects = models.ManyToManyField('projects.Project', related_name='engineers', verbose_name='Проекты',blank=True)

    def experience(self):
        today = datetime.date.today()
        years = today.year - self.worker_avt.start_date.year
        months = today.month - self.worker_avt.start_date.month
        days = today.day - self.worker_avt.start_date.day
        if days < 0:
            months -= 1
            days += 30  # приблизительно
        if months < 0:
            years -= 1
            months += 12

        return f"{years} лет, {months} месяцев"

    # def __str__(self):
    #     return self.worker_avt.full_name if self.worker_avt else 'Не определён'

    def __str__(self):
        return f"{self.worker_avt.full_name} - {self.role.name if self.role else 'Без должности'}"

    def photo_preview(self):
        if self.photo:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', self.photo.url)
        return "Нет фото"
    photo_preview.short_description = 'Превью фото'



class AutomationDepartment(models.Model):
    name = models.ForeignKey('departments.Department', on_delete=models.CASCADE, verbose_name='Название отдела')
    description = models.TextField(blank=True, verbose_name='Описание')
    workers = models.ManyToManyField('avtomatizations.AutomationEngineer', related_name='automation_departments', verbose_name='Сотрудники')

    def __str__(self):
        return self.name.name
